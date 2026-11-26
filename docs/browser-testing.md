# Browser and autoplay checks

Install dependencies and official Playwright browsers:

```sh
npm ci --no-audit --no-fund
npx playwright install chromium firefox webkit
npm run check:cross-browser
```

The test server builds the current sources into `_site` before serving them. It
does not reuse an unrelated server on the same port. To use a different port:

```sh
PLAYWRIGHT_PORT=4186 npm run check:cross-browser
```

Run the original Chromium regression suite with
`npm run check:browser -- --project=chromium`, or all projects with
`npm run check:browser`. View results with `npx playwright show-report`.

## Coverage

The new suite runs the same scenarios in Chromium, Firefox (Gecko) and WebKit,
at a 1440px desktop viewport and a narrow mobile profile. Chromium uses the
Pixel 7 descriptor; WebKit uses iPhone 13. Firefox does not support Playwright's
`isMobile` emulation: its mobile project is explicitly a 390px touch viewport,
not an actual Android Firefox session.

- Both iOS and Android video sets on first load, without clicking a play button.
- Actual MP4 bytes decode, have no media error, and `currentTime` advances.
- Hero, panel-reading and auto-scroll demos start on entering the viewport.
- Offscreen pause, reentry and source changes via platform buttons.
- Blocked `play()` preserves the poster and manual native controls.
- Reduced-motion preference suppresses automatic playback, including switches.
- Changing reduced motion at runtime pauses/resumes visible media. Missing
  visibility-observer support and failed media requests retain manual fallbacks.
- Homepage plus Duo, Help, comparison, Kavita and Komga pages have a visible
  heading and no document-level horizontal overflow; homepage images and menu
  work. Native image proportions are checked for the hero video.
- Screenshots for each engine/profile are attached to the HTML report and saved
  under `output/browser-preview/` for visual inspection. These are evidence for
  review, not pixel-identical cross-engine guarantees or approved golden files.

Gesture-free playback is observed through page-owned console telemetry before
DOM evaluation, with zero pointer/touch/key input. Some automation evaluations
grant browser user activation, so tests avoid calling `evaluate()` or `play()`
to make autoplay pass. Chromium's permissive autoplay default argument is not
enabled; Firefox blocks audible autoplay. The fallback test deliberately mocks
`play()` rejection; the normal playback tests never mock the media APIs.

Both platforms use the same markup. Tests select their initial media set by
substituting only the existing `applyPlatform` initialization in served HTML;
videos, CSS, handlers and real media responses remain unchanged. This checks
each media set before a platform-button click could authorize playback.

## CI and limits

The site-quality workflow runs the cross-browser matrix on macOS so WebKit uses
native MP4 support. It preserves reports, screenshots and failure traces for
14 days. Original Chromium checks and Lighthouse stay in the Linux job.

Playwright WebKit is not the branded Safari app; Playwright Firefox is a patched
Firefox build, not Firefox for Android. Mobile profiles do not reproduce every
real-device policy. Autoplay can be denied by user/site settings, Low Power Mode,
data-saving settings or OS policy; the site must not bypass them. Keep native
controls and a poster for that case. With reduced motion, playback is purposely
manual. Streaming setup-guide videos remain user-controlled (they include
spoken audio/captions); only the muted homepage previews auto-start.

Before release, check a physical iPhone in Safari and Firefox, Android Chrome
and Firefox, and desktop Safari/Firefox/Chrome: normal power, Low Power Mode,
autoplay denied, reduced motion, page scroll, both platform choices, and
background/foreground transitions. Confirm audible playback never starts by
itself and manual controls remain usable when autoplay is denied.

References: [WebKit media policies](https://webkit.org/blog/6784/new-video-policies-for-ios/)
and [Playwright browser/codec limitations](https://playwright.dev/docs/browsers).
