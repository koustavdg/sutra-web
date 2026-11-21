// Generate a native, branded sharing card; no network or image-generation service.
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('@playwright/test');
async function main() {
  const root = path.resolve(__dirname, '..');
  const icon = fs.readFileSync(path.join(root, 'assets/app-icon.png')).toString('base64');
  const svg = fs.readFileSync(path.join(root, 'templates/social-card.svg'), 'utf8')
    .replace('{{icon_data}}', 'data:image/png;base64,' + icon);
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 1200, height: 630}, deviceScaleFactor: 1});
    await page.setContent('<html><body style="margin:0">' + svg + '</body></html>');
    await page.locator('svg image').evaluate(el => new Promise(resolve => {
      const image = new Image(); image.onload = resolve; image.onerror = resolve;
      image.src = el.getAttribute('href');
    }));
    await page.screenshot({path: path.join(root, 'assets/social-card.png')});
  } finally { await browser.close(); }
}
main().catch(error => {console.error(error); process.exitCode = 1;});
