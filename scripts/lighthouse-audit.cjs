// Measure each landing page three times and report the median mobile scores.
const { spawnSync } = require('node:child_process');
const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const http = require('node:http');

const pages = ['kavita-reader', 'komga-reader', 'comic-panel-reader', 'opds-reader', 'calibre-reader'];
const reportDir = fs.mkdtempSync(path.join(os.tmpdir(), 'sutra-lighthouse-'));
const binary = path.resolve('node_modules/.bin/lighthouse');

function waitForServer(attempt = 0) {
  return new Promise((resolve, reject) => {
    const request = http.get('http://127.0.0.1:4173/', response => {
      response.resume();
      response.statusCode === 200 ? resolve() : reject(new Error(`Server returned ${response.statusCode}`));
    });
    request.on('error', error => {
      if (attempt >= 30) reject(error);
      else setTimeout(() => waitForServer(attempt + 1).then(resolve, reject), 250);
    });
  });
}

async function main() {
  await waitForServer();
  let failed = false;
  for (const page of pages) {
    const scores = { performance: [], accessibility: [] };
    for (let run = 1; run <= 3; run++) {
      const report = path.join(reportDir, `${page}-${run}.json`);
      const result = spawnSync(binary, [
        `http://127.0.0.1:4173/${page}.html`,
        '--only-categories=performance,accessibility', '--output=json',
        `--output-path=${report}`, '--quiet',
        '--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage --disable-gpu',
      ], { encoding: 'utf8', timeout: 120000 });
      if (result.error || result.status !== 0) {
        throw new Error(`Lighthouse failed for ${page} run ${run}: ${result.error || result.stderr}`);
      }
      const data = JSON.parse(fs.readFileSync(report, 'utf8'));
      for (const category of Object.keys(scores)) {
        const score = data.categories?.[category]?.score;
        if (typeof score !== 'number') throw new Error(`Missing ${category} score for ${page} run ${run}`);
        scores[category].push(Math.round(score * 100));
      }
    }
    const median = values => [...values].sort((a, b) => a - b)[1];
    const performance = median(scores.performance);
    const accessibility = median(scores.accessibility);
    console.log(`${page}: performance ${scores.performance.join('/')} (median ${performance}); accessibility ${scores.accessibility.join('/')} (median ${accessibility})`);
    if (performance < 85 || accessibility < 95) failed = true;
  }
  if (failed) throw new Error('One or more landing-page medians fell below the agreed budgets (85 performance, 95 accessibility).');
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
