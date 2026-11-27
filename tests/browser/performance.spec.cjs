const { test, expect } = require('@playwright/test');

test('local fonts and responsive images load and follow platform switches', async ({ page }) => {
  const externalFonts = [];
  page.on('request', request => { if (/fonts\.(googleapis|gstatic)\.com/.test(request.url())) externalFonts.push(request.url()); });
  await page.setViewportSize({width: 390, height: 844});
  await page.goto('/');
  await page.evaluate(() => document.fonts.ready);
  expect(await page.evaluate(() => document.fonts.check('600 20px Spectral'))).toBe(true);
  expect(externalFonts).toEqual([]);
  await expect(page.locator('#current-releases')).toContainText('iOS 2.5.0 · Android 1.3.0');
  for (const platform of ['android', 'ios']) {
    await page.locator(`[data-plat="${platform}"]`).first().click();
    const image = page.locator('#shot-lib');
    await image.scrollIntoViewIfNeeded();
    await expect(image).toHaveAttribute('srcset', new RegExp(`${platform}-(library|hero)`));
    await expect.poll(() => image.evaluate(img => img.complete && img.naturalWidth > 0 && img.currentSrc)).toContain(`${platform}-library-`);
  }
});

test('text-only release order and tablet claims agree with machine-readable files', async ({ browser }) => {
  const context = await browser.newContext({javaScriptEnabled: false});
  const page = await context.newPage();
  await page.goto('/');
  await expect(page.locator('#rm-src .version-num').first()).toHaveText('2.5.0');
  for (const file of ['/', '/help.html', '/compare-readers.html', '/sutra-vs-panels.html', '/sutra-vs-readest.html']) {
    await page.goto(file);
    await expect(page.locator('body')).toContainText('Two-page side-by-side layouts are available on iPad and Android tablets in landscape.');
    await expect(page.locator('body')).toContainText('Improved comic-spread detection and page pairing are in development');
  }
  await context.close();
});
