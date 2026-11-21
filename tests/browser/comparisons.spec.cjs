const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const slugs = ['compare-readers', 'sutra-vs-readest', 'sutra-vs-panels'];

for (const width of [390, 1440]) {
  for (const slug of slugs) {
    test(`${slug}: discoverable without JavaScript at ${width}px`, async ({ browser }) => {
      const context = await browser.newContext({ javaScriptEnabled: false, viewport: { width, height: 900 } });
      const page = await context.newPage();
      const response = await page.goto(`/${slug}.html`);
      expect(response.status()).toBe(200);
      await expect(page.locator('h1')).toHaveCount(1);
      await expect(page.locator('link[rel=canonical]')).toHaveAttribute('href', `https://sutra-reader.com/${slug}.html`);
      await expect(page.locator('meta[name=robots]')).not.toHaveAttribute('content', /noindex/);
      await expect(page.locator('main')).toContainText('Questions about this comparison');
      await expect(page.locator('#sources')).toContainText('2026-11-21');
      const faq = page.locator('#comparison-questions details').first();
      await faq.locator('summary').click();
      await expect(faq).toHaveAttribute('open', '');
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth)).toBe(true);
      await page.screenshot({ path: `output/comparison-preview/${slug}-${width}.png`, fullPage: true });
      await context.close();
    });
  }
}

test('comparisons are linked from home and setup guides, with accessible tables', async ({ page }) => {
  await page.goto('/');
  await expect(page.locator('#reading-guides a[href="compare-readers.html"]')).toBeVisible();
  for (const slug of ['kavita-reader', 'komga-reader', 'comic-panel-reader', 'calibre-reader', 'opds-reader']) {
    await page.goto(`/${slug}.html`);
    await expect(page.locator('.related a[href="compare-readers.html"]')).toHaveCount(1);
  }
  for (const slug of slugs) {
    await page.goto(`/${slug}.html`);
    const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
    expect(results.violations.filter(v => ['serious', 'critical'].includes(v.impact))).toEqual([]);
    await expect(page.locator('table caption')).toHaveCount(1);
    await expect(page.locator('table th[scope=row]').first()).toBeVisible();
  }
});
