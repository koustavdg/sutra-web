// Repeatable cold-cache mobile lab measurements. Never installs site tracking.
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const { spawnSync } = require('node:child_process');
const { chromium } = require('@playwright/test');

const defaults = ['/', '/compare-readers.html', '/kavita-reader.html', '/komga-reader.html',
  '/comic-panel-reader.html', '/opds-reader.html', '/calibre-reader.html'];
const keys = ['performance', 'accessibility', 'seo', 'fcp_ms', 'lcp_ms', 'tbt_ms', 'cls', 'bytes'];
function meetsBudget(page) {
  // Retain existing guide budgets. New home/hub performance measurements are
  // reporting-only until their hosted-runner baseline is calibrated.
  const guide = defaults.slice(2).includes(page.path);
  return (!guide || page.median.performance >= 85)
    && page.median.accessibility >= 95 && page.median.seo >= 95;
}
function median(values) {
  const sorted = [...values].sort((a, b) => a - b);
  const mid = Math.floor(sorted.length / 2);
  return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
}
function summarize(reports) {
  return Object.fromEntries(keys.map(key => [key, median(reports.map(row => row[key]))]));
}
function sample(report) {
  if (report.runtimeError) throw new Error(report.runtimeError.message);
  const metric = id => {
    const value = report.audits[id]?.numericValue;
    if (!Number.isFinite(value)) throw new Error(`Missing metric: ${id}`);
    return value;
  };
  const scores = Object.fromEntries(['performance', 'accessibility', 'seo'].map(key => {
    const value = report.categories[key]?.score;
    if (!Number.isFinite(value)) throw new Error(`Missing score: ${key}`);
    return [key, Math.round(value * 100)];
  }));
  return { ...scores, fcp_ms: metric('first-contentful-paint'), lcp_ms: metric('largest-contentful-paint'),
    tbt_ms: metric('total-blocking-time'), cls: metric('cumulative-layout-shift'), bytes: metric('total-byte-weight') };
}
function markdown(result, previous) {
  const out = [`# Sutra mobile performance — ${result.label}`, '',
    `${result.runs} sequential cold-cache runs per page; medians. Captured ${result.capturedAt}.`, '',
    `Base URL: ${result.baseUrl}. Lighthouse ${result.lighthouseVersion}; Chromium ${result.browserVersion}.`, '',
    'Simulated mobile lab results, not field Core Web Vitals, SEO rankings or AI citation measurements.',
    'Compare the same pages, run count, Lighthouse version, hardware, browser and hosting conditions. Local before/after tests do not measure CDN, compression or public-network latency.', '',
    '| Page | Performance | LCP (s) | TBT (ms) | CLS | Transfer (KiB) | Accessibility | SEO |',
    '|---|---:|---:|---:|---:|---:|---:|---:|'];
  for (const row of result.pages) {
    const m = row.median;
    out.push(`| ${row.path} | ${m.performance} | ${(m.lcp_ms / 1000).toFixed(2)} | ${m.tbt_ms.toFixed(0)} | ${m.cls.toFixed(3)} | ${(m.bytes / 1024).toFixed(1)} | ${m.accessibility} | ${m.seo} |`);
  }
  if (previous) {
    if (result.runs !== previous.runs || result.lighthouseVersion !== previous.lighthouseVersion || result.browserVersion !== previous.browserVersion || JSON.stringify(result.machine) !== JSON.stringify(previous.machine)) {
      throw new Error('Incompatible baseline: keep run count, Lighthouse, browser and machine identical.');
    }
    if (JSON.stringify(result.pages.map(p => p.path)) !== JSON.stringify(previous.pages.map(p => p.path))) throw new Error('Baseline pages differ.');
    for (const setting of ['formFactor', 'throttlingMethod', 'throttling', 'screenEmulation']) {
      if (JSON.stringify(result.settings?.[setting]) !== JSON.stringify(previous.settings?.[setting])) throw new Error(`Baseline settings differ: ${setting}`);
    }
    out.push('', `## Change from ${previous.label}`, '', 'Positive performance deltas are better; negative time/byte deltas are better. These are observations, not guaranteed effects.', '',
      '| Page | Performance Δ | LCP Δ (s) | Transfer Δ (KiB) |', '|---|---:|---:|---:|');
    for (const row of result.pages) {
      const before = previous.pages.find(p => p.path === row.path).median, after = row.median;
      out.push(`| ${row.path} | ${after.performance - before.performance} | ${((after.lcp_ms - before.lcp_ms) / 1000).toFixed(2)} | ${((after.bytes - before.bytes) / 1024).toFixed(1)} |`);
    }
  }
  out.push('', 'Raw Lighthouse JSON reports and per-run values are retained beside this report. Each score/metric median is calculated independently.', '');
  return out.join('\n');
}
async function main(args = process.argv.slice(2)) {
  const option = (name, fallback) => { const i = args.indexOf(name); return i === -1 ? fallback : args[i + 1]; };
  const baseUrl = option('--base-url', 'http://127.0.0.1:4173');
  const label = option('--label', 'measurement');
  const runs = Number(option('--runs', '3'));
  if (!Number.isInteger(runs) || runs < 1 || runs > 10) throw new Error('--runs must be 1–10');
  const pages = option('--pages', '').split(',').filter(Boolean);
  const directory = path.resolve(option('--out', `output/performance/${label}`));
  if (fs.existsSync(path.join(directory, 'results.json'))) throw new Error('Output already contains results; choose a new --out directory.');
  fs.mkdirSync(directory, { recursive: true });
  const result = { schemaVersion: 1, label, baseUrl, runs, capturedAt: new Date().toISOString(),
    machine: { platform: os.platform(), arch: os.arch(), cpu: os.cpus()[0].model },
    gitCommit: spawnSync('git', ['rev-parse', 'HEAD'], { encoding: 'utf8' }).stdout.trim(),
    dirty: Boolean(spawnSync('git', ['diff', '--stat'], { encoding: 'utf8' }).stdout.trim()),
    pages: [] };
  for (const [index, page] of (pages.length ? pages : defaults).entries()) {
    const reports = [];
    for (let run = 1; run <= runs; run++) {
      const filename = `${index}-${run}.json`, output = path.join(directory, filename);
      const child = spawnSync(path.resolve('node_modules/.bin/lighthouse'), [new URL(page, baseUrl).href,
        '--only-categories=performance,accessibility,seo', '--form-factor=mobile', '--throttling-method=simulate',
        '--output=json', `--output-path=${output}`, '--quiet',
        '--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage --disable-gpu'],
      { env: { ...process.env, CHROME_PATH: chromium.executablePath() }, encoding: 'utf8', timeout: 150_000 });
      if (child.error || child.status !== 0) throw new Error(`Lighthouse failed on ${page}: ${child.error || child.stderr}`);
      const data = JSON.parse(fs.readFileSync(output, 'utf8'));
      result.lighthouseVersion = data.lighthouseVersion;
      result.browserVersion = data.environment?.hostUserAgent;
      result.settings = data.configSettings;
      reports.push({ ...sample(data), report: filename });
      console.log(`${label} ${page} ${run}/${runs}: performance ${reports.at(-1).performance}; LCP ${reports.at(-1).lcp_ms.toFixed(0)}ms`);
    }
    result.pages.push({ path: page, samples: reports, median: summarize(reports) });
    fs.writeFileSync(path.join(directory, 'partial.json'), JSON.stringify(result, null, 2));
  }
  const compare = option('--compare-to', null);
  const report = markdown(result, compare && JSON.parse(fs.readFileSync(compare, 'utf8')));
  fs.writeFileSync(path.join(directory, 'results.json'), JSON.stringify(result, null, 2));
  fs.writeFileSync(path.join(directory, 'report.md'), report);
  console.log(`Saved ${directory}/report.md`);
  return result;
}
module.exports = { median, summarize, sample, markdown, main, meetsBudget };
if (require.main === module) main().catch(error => { console.error(error); process.exitCode = 1; });
