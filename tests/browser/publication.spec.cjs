const {test, expect} = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test('both privacy policies are readable without JavaScript', async ({browser}) => {
  const context = await browser.newContext({javaScriptEnabled:false});
  const page = await context.newPage();
  await page.goto('/privacy.html');
  await expect(page.locator('#ios')).toBeVisible();
  await expect(page.locator('#android')).toBeVisible();
  await expect(page.locator('#ios')).toContainText('iOS Keychain');
  await expect(page.locator('#android')).toContainText('Android Keystore');
  await expect(page.locator('h1')).toHaveCount(1);
  await context.close();
});

test('privacy tabs work even when the public source is unavailable', async ({page}) => {
  await page.route('https://raw.githubusercontent.com/**', route => route.abort());
  await page.goto('/privacy.html#android');
  await expect(page.locator('#android')).toBeVisible();
  await expect(page.locator('#ios')).toBeHidden();
  await page.locator('#tab-ios').click();
  await expect(page.locator('#ios')).toContainText('iOS Keychain');
  await expect(page.locator('#android')).toBeHidden();
  await expect(page.locator('#tab-ios')).toHaveAttribute('aria-selected','true');
});

test('entitlements and sharing metadata are readable without scripts', async ({browser}) => {
  const context = await browser.newContext({javaScriptEnabled:false});
  const page = await context.newPage();
  await page.goto('/');
  await expect(page.locator('#compare')).toContainText('Included');
  await expect(page.locator('#compare')).toContainText('Pro required');
  await expect(page.locator('#compare')).toContainText('$6.99 USD');
  await expect(page.locator('main')).toHaveCount(1);
  await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /social-card.png$/);
  await expect(page.locator('#hero-video')).toHaveAttribute('controls', '');
  await context.close();
});

test('offscreen videos defer downloads, play when visible and pause when hidden', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  const requests=[];
  page.on('request', req => {if(req.url().includes('.mp4')) requests.push(req.url());});
  await page.goto('/');
  await page.waitForTimeout(700);
  expect(requests.filter(url=>/05-comics|06-autoscroll/.test(url))).toEqual([]);
  const video = page.locator('#hero-video');
  await video.scrollIntoViewIfNeeded();
  await expect.poll(()=>video.evaluate(v=>!v.paused)).toBe(true);
  await page.locator('#compare').scrollIntoViewIfNeeded();
  await expect.poll(()=>video.evaluate(v=>v.paused)).toBe(true);
  await page.locator('.strip [data-plat="android"]').scrollIntoViewIfNeeded();
  await page.locator('.strip [data-plat="android"]').click();
  await expect(page.locator('#shot-comics')).toHaveAttribute('src', /android/);
  await expect(page.locator('#shot-scroll').locator('..')).toHaveAttribute('poster', /android-autoscroll/);
});

test('reduced motion offers controls without autoplay', async ({page}) => {
  await page.emulateMedia({reducedMotion:'reduce'});
  await page.goto('/');
  const video=page.locator('#hero-video');
  await video.scrollIntoViewIfNeeded();
  await expect(video).toHaveAttribute('controls','');
  await expect.poll(()=>video.evaluate(v=>v.paused)).toBe(true);
});

test('home, Help and privacy have no serious accessibility violations', async ({page}) => {
  await page.setViewportSize({width:390,height:844});
  await page.route('https://raw.githubusercontent.com/**', route => route.abort());
  for (const url of ['/', '/help.html', '/privacy.html']) {
    await page.goto(url);
    const results=await new AxeBuilder({page}).withTags(['wcag2a','wcag2aa','wcag21a','wcag21aa']).analyze();
    expect(results.violations.filter(v=>['serious','critical'].includes(v.impact))).toEqual([]);
  }
});
