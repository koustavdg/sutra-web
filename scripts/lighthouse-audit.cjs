// CI uses the same seven-page, three-run measurement loop as local audits.
const http = require('node:http');

function waitForServer(attempt = 0) {
  return new Promise((resolve, reject) => {
    const request = http.get('http://127.0.0.1:4173/', response => {
      response.resume();
      response.statusCode === 200 ? resolve() : reject(new Error(`Server returned ${response.statusCode}`));
    });
    request.setTimeout(1000, () => request.destroy());
    request.on('error', error => {
      if (attempt >= 30) reject(error);
      else setTimeout(() => waitForServer(attempt + 1).then(resolve, reject), 250);
    });
  });
}

async function main() {
  await waitForServer();
  // Use the same durable reports, page set and medians as local before/after runs.
  const loop = require('./performance-loop.cjs');
  const label = `ci-${process.env.GITHUB_RUN_ID || Date.now()}`;
  const result = await loop.main(['--label', label, '--out', `output/performance/${label}`]);
  for (const page of result.pages) {
    if (!loop.meetsBudget(page)) {
      throw new Error(`${page.path} below budgets: existing guide performance ≥85, all-page accessibility/SEO ≥95; see saved reports.`);
    }
  }
}

main().catch(error => { console.error(error.message); process.exitCode = 1; });
