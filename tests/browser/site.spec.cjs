const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const pages = [
  'kavita-reader.html',
  'komga-reader.html',
  'comic-panel-reader.html',
  'opds-reader.html',
  'calibre-reader.html',
];

for (const width of [390, 1440]) {
  test.describe(`${width}px viewport`, () => {
    test.use({ viewport: { width, height: 900 } });

    for (const path of pages) {
      test(`${path}: readable without JavaScript and no horizontal overflow`, async ({ browser }) => {
        const context = await browser.newContext({
          viewport: { width, height: 900 },
          javaScriptEnabled: false,
        });
        const page = await context.newPage();
        const response = await page.goto(path);
        expect(response.status()).toBe(200);
        await expect(page.locator('h1')).toHaveCount(1);
        await expect(page.locator('main')).toContainText('Frequently asked questions');
        expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
        const firstFaq = page.locator('.faq details').first();
        await firstFaq.locator('summary').focus();
        await page.keyboard.press('Enter');
        await expect(firstFaq).toHaveAttribute('open', '');
        await context.close();
      });
    }
  });
}

test('landing pages pass axe and overflow checks at mobile, 200%-zoom width, and desktop', async ({ page }) => {
  for (const width of [390, 720, 1440]) {
    for (const path of pages) {
      await page.setViewportSize({ width, height: 900 });
      await page.goto(path);
      const results = await new AxeBuilder({ page }).withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa']).analyze();
      const serious = results.violations.filter(v => ['serious', 'critical'].includes(v.impact));
      expect(serious, `${path} at ${width}px: ${JSON.stringify(serious.map(v => ({ id: v.id, nodes: v.nodes.length })))}`).toEqual([]);
      expect(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth)).toBe(true);
    }
  }
});

test('shared streaming demo plays and provides captions and a transcript', async ({ page }) => {
  for (const path of ['kavita-reader.html', 'komga-reader.html']) {
    await page.goto(path);
    const video = page.locator('video');
    await expect(video).toHaveAttribute('controls', '');
    await expect(video.locator('track[kind="captions"]')).toHaveCount(1);
    await expect(page.locator('details').filter({ hasText: 'Video transcript' })).toContainText('without first downloading the full book');
    await video.evaluate(async element => {
      element.muted = true;
      await element.play();
    });
    await expect.poll(() => video.evaluate(element => element.currentTime)).toBeGreaterThan(0);
    await video.evaluate(element => element.pause());
    const captions = await page.request.get('/assets/demos/reading-demo-ios.vtt');
    expect(captions.ok()).toBeTruthy();
    expect(await captions.text()).toContain('without downloading the full book first');
  }
});

test('existing navigation, Help deep links and privacy tabs still work', async ({ page }) => {
  await page.route('https://raw.githubusercontent.com/**', route => route.abort());
  await page.goto('/');
  await page.locator('#hamburger').click();
  await expect(page.locator('#hamburger')).toHaveAttribute('aria-expanded', 'true');
  await expect(page.locator('#ham-menu a[href="help.html"]')).toBeVisible();
  await page.keyboard.press('Escape');
  await expect(page.locator('#hamburger')).toHaveAttribute('aria-expanded', 'false');

  await page.goto('/help.html#kavita');
  await expect(page.locator('details#kavita')).toHaveAttribute('open', '');
  await expect(page.locator('details#kavita')).toContainText('OPDS');

  await page.goto('/privacy.html');
  await page.locator('#tab-android').click();
  await expect(page.locator('#tab-android')).toHaveAttribute('aria-selected', 'true');
  await expect(page.locator('#prose')).toContainText('Android');
});
