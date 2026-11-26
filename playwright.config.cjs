const { defineConfig, devices } = require('@playwright/test');

const crossBrowserSpec = '**/cross-browser.spec.cjs';
const port = Number(process.env.PLAYWRIGHT_PORT || 4173);

module.exports = defineConfig({
  testDir: './tests/browser',
  fullyParallel: true,
  workers: 2,
  reporter: [['list'], ['html', { open: 'never' }]],
  use: {
    baseURL: `http://127.0.0.1:${port}`,
    headless: true,
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [
    { name: 'chromium', testIgnore: crossBrowserSpec, use: { browserName: 'chromium' } },
    ...['chromium', 'firefox', 'webkit'].map(browserName => ({
      name: `${browserName}-desktop`, testMatch: crossBrowserSpec,
      use: { browserName, viewport: { width: 1440, height: 1000 }, launchOptions: browserName === 'firefox'
        ? { firefoxUserPrefs: { 'media.autoplay.default': 1 } }
        : browserName === 'chromium' ? { ignoreDefaultArgs: ['--autoplay-policy=no-user-gesture-required'] } : {} },
    })),
    { name: 'chromium-mobile', testMatch: crossBrowserSpec, use: { ...devices['Pixel 7'], browserName: 'chromium',
      launchOptions: { ignoreDefaultArgs: ['--autoplay-policy=no-user-gesture-required'] } } },
    // Gecko has no Playwright isMobile emulation: this is a narrow, touch viewport.
    { name: 'firefox-mobile-viewport', testMatch: crossBrowserSpec,
      use: { browserName: 'firefox', viewport: { width: 390, height: 844 }, hasTouch: true,
        launchOptions: { firefoxUserPrefs: { 'media.autoplay.default': 1 } } } },
    { name: 'webkit-mobile', testMatch: crossBrowserSpec, use: { ...devices['iPhone 13'], browserName: 'webkit' } },
  ],
  webServer: {
    command: `python3 scripts/build_site.py && python3 -m http.server ${port} --bind 127.0.0.1 --directory _site`,
    url: `http://127.0.0.1:${port}/`,
    reuseExistingServer: false,
    timeout: 120_000,
    stdout: 'pipe',
    stderr: 'pipe',
  },
});
