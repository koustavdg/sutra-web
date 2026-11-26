const { test, expect } = require('@playwright/test');
const fs = require('node:fs/promises');
const path = require('node:path');

test.setTimeout(60_000);
const playback = new WeakMap();

test.beforeEach(async ({ page }) => {
  // Read page-owned telemetry via console events. DOM queries/evaluate can grant
  // user activation in Playwright, so do neither before gesture-free playback.
  const samples = {};
  playback.set(page, samples);
  page.on('console', message => {
    if (message.text().startsWith('SUTRA_MEDIA:')) {
      const sample = JSON.parse(message.text().slice(12));
      samples[sample.id] = sample;
    }
  });
  page.on('framenavigated', frame => { if (frame === page.mainFrame()) Object.keys(samples).forEach(key => delete samples[key]); });
  await page.addInitScript(() => {
    let inputEvents = 0;
    ['pointerdown', 'touchstart', 'keydown'].forEach(name => document.addEventListener(name, () => inputEvents++, true));
    setInterval(() => document.querySelectorAll('video').forEach(v => {
      console.info('SUTRA_MEDIA:' + JSON.stringify({ id: v.id || v.querySelector('source')?.id,
        playing: !v.paused, ready: v.readyState >= 2,
        time: v.currentTime, width: v.videoWidth, muted: v.muted, inline: v.hasAttribute('playsinline'),
        autoplay: v.autoplay, controls: v.controls, inputEvents,
        error: v.error && `${v.error.code}: ${v.error.message}` }));
    }), 100);
    document.addEventListener('DOMContentLoaded', () => {
      if (location.hash.startsWith('#test-')) {
        document.getElementById(location.hash.slice(6))?.closest('video')?.scrollIntoView({ behavior: 'instant', block: 'center' });
      }
    });
  });
});

function state(page, id) { return playback.get(page)[id] || {}; }

async function advancing(page, id) {
  await expect.poll(() => state(page, id), { timeout: 20_000 }).toMatchObject({ playing: true, ready: true, error: null });
  expect(state(page, id).width).toBeGreaterThan(0);
  const before = state(page, id).time;
  await expect.poll(() => state(page, id).time, { timeout: 10_000 }).toBeGreaterThan(before + 0.15);
}

async function screenshot(page, testInfo, name) {
  await fs.mkdir('output/browser-preview', { recursive: true });
  const filename = path.join('output/browser-preview', `${testInfo.project.name}-${name}.png`);
  await page.screenshot({ path: filename });
  await testInfo.attach(name, { path: filename, contentType: 'image/png' });
}

for (const platform of ['ios', 'android']) {
  test(`${platform}: videos autoplay without a gesture and resume on reentry`, async ({ page }, testInfo) => {
    // Route the public HTML only to select either existing platform on first load.
    // Real video bytes, codecs, media APIs and browser autoplay policy remain untouched.
    await page.route('**/*', async route => {
      if (route.request().resourceType() !== 'document') return route.continue();
      const response = await route.fetch();
      const source = await response.text();
      const initializer = "applyPlatform(document.documentElement.classList.contains('is-android') ? 'android' : 'ios', false);";
      expect(source).toContain(initializer);
      const html = source.replace(initializer, `applyPlatform('${platform}', false);`);
      await route.fulfill({ response, body: html });
    });
    await page.goto('/#hero-video');
    const hero = page.locator('#hero-video');
    await advancing(page, 'hero-video');
    expect(state(page, 'hero-video')).toMatchObject({ inputEvents: 0, muted: true, inline: true });
    await expect(hero.locator('source')).toHaveAttribute('src', new RegExp(`preview-${platform}`));
    await expect(page.locator('#hero-back')).toBeVisible();
    const bounds = await hero.boundingBox();
    expect(bounds.height / bounds.width).toBeCloseTo(1920 / 886, 1);
    await screenshot(page, testInfo, `${platform}-hero-playing`);

    for (const id of ['shot-comics', 'shot-scroll']) {
      await page.goto(`/?autoplay-case=${id}#test-${id}`);
      await advancing(page, id);
      expect(state(page, id).inputEvents).toBe(0);
    }
    await page.locator('#compare').scrollIntoViewIfNeeded();
    await expect.poll(() => hero.evaluate(v => v.paused)).toBe(true);
    await hero.scrollIntoViewIfNeeded();
    await advancing(page, 'hero-video');
    await page.locator('.hero-tog [data-plat]').filter({ hasText: platform === 'ios' ? 'Android' : 'iOS' }).click();
    await expect(hero.locator('source')).toHaveAttribute('src', new RegExp(`preview-${platform === 'ios' ? 'android' : 'ios'}`));
    await advancing(page, 'hero-video');
  });
}

test('blocked autoplay keeps a poster and usable controls', async ({ page }) => {
  await page.addInitScript(() => {
    HTMLMediaElement.prototype.play = function() { return Promise.reject(new DOMException('User policy', 'NotAllowedError')); };
  });
  await page.goto('/');
  const hero = page.locator('#hero-video');
  await hero.scrollIntoViewIfNeeded();
  await expect(hero).toHaveAttribute('controls', '');
  await expect(hero).toHaveAttribute('poster', /poster/);
});

test('reduced motion disables all automatic playback, including platform switches', async ({ page }) => {
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await page.goto('/');
  const hero = page.locator('#hero-video');
  await hero.scrollIntoViewIfNeeded();
  for (const platform of ['ios', 'android']) {
    await page.locator(`.hero-tog [data-plat="${platform}"]`).click();
    await expect(hero).toHaveAttribute('controls', '');
    expect(await hero.evaluate(v => v.paused && !v.autoplay)).toBe(true);
  }
});

test('changing reduced motion pauses and then resumes visible media', async ({ page }) => {
  await page.goto('/#hero-video');
  await advancing(page, 'hero-video');
  await page.emulateMedia({ reducedMotion: 'reduce' });
  await expect.poll(() => state(page, 'hero-video')).toMatchObject({ playing: false, autoplay: false, controls: true });
  await page.emulateMedia({ reducedMotion: 'no-preference' });
  await advancing(page, 'hero-video');
});

test('without visibility observer the poster and manual controls remain', async ({ page }) => {
  await page.addInitScript(() => { delete window.IntersectionObserver; });
  await page.goto('/#hero-video');
  await expect.poll(() => state(page, 'hero-video')).toMatchObject({ playing: false, autoplay: false, controls: true });
  await expect(page.locator('#hero-video')).toHaveAttribute('poster', /poster/);
});

test('failed media requests retain the manual fallback', async ({ page }) => {
  let failedRequests = 0;
  page.on('requestfailed', request => { if (request.url().includes('.mp4')) failedRequests++; });
  await page.route('**/*.mp4*', route => route.abort());
  await page.goto('/#hero-video');
  await expect.poll(() => failedRequests).toBeGreaterThan(0);
  // A failed <source> need not populate video.error or reset paused in Gecko.
  // No frame decodes/time advances, and native controls must remain available.
  await expect.poll(() => state(page, 'hero-video')).toMatchObject({ ready: false, time: 0, controls: true });
  await expect(page.locator('#hero-video')).toHaveAttribute('poster', /poster/);
});

test('home and key pages preserve layout, images and navigation', async ({ page }, testInfo) => {
  for (const url of ['/', '/iphone-duo.html', '/help.html', '/compare-readers.html', '/kavita-reader.html', '/komga-reader.html']) {
    await page.goto(url);
    await expect(page.locator('h1')).toHaveCount(1);
    await expect(page.locator('h1')).toBeVisible();
    expect(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1)).toBe(true);
    // Image load assertions catch silent error-placeholder substitutions as well.
    if (url === '/') {
      await expect(page.locator('#hero-back')).toBeVisible();
      await expect.poll(() => page.locator('#hero-back').evaluate(img => img.naturalWidth)).toBeGreaterThan(0);
      await page.locator('#hamburger').click();
      await expect(page.locator('#ham-menu a[href="help.html"]')).toBeVisible();
      await page.keyboard.press('Escape');
      await screenshot(page, testInfo, 'homepage-layout');
    } else {
      await screenshot(page, testInfo, url.slice(1, -5));
    }
  }
});
