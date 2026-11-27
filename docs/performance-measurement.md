# Performance and discoverability measurement

## What changed

- Owner-confirmed on November 26, 2026: landscape two-page layouts already ship
  on iPad and Android tablets. Improved comic-spread detection and page pairing
  are still in development. Shared product facts feed the homepage, FAQ,
  comparisons, and both LLM files.
- Current public versions are iOS 2.5.0 and Android 1.3.0. One shared record
  supplies the homepage/changelog summary and LLM files. Historical release
  notes retain their original versions and dates; text-only roadmap readers
  now encounter 2.5.0 before the older shared release.
- Font faces are served locally, with the same families/weights and bundled OFL
  licenses. No Google Fonts stylesheet or font request is needed at runtime.
- Original artwork is preserved. WebP derivatives supply responsive screenshots
  and icons; posters are compressed. Platform switching updates `srcset` and
  `src` together. Schema/social images retain their original public asset URLs.

## Repeatable mobile lab loop

Install the pinned npm dependencies and Playwright Chromium. Build the site and
serve it in a separate terminal:

```sh
python3 scripts/build_site.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory _site
```

Measure the homepage, comparison hub and five reading guides, three times each,
sequentially:

```sh
npm run measure:performance -- --label before --out output/performance/before
```

After changing and rebuilding the site, run:

```sh
npm run measure:performance -- --label after --out output/performance/after --compare-to output/performance/before/results.json
```

For live post-deployment measurement, use a fresh output directory and
`--base-url https://sutra-reader.com/`. Compare live against live, not localhost.
`--pages /,/compare-readers.html` permits a shorter diagnostic run; the full
seven-page loop remains the default. Do not overwrite earlier results.

Every run retains raw Lighthouse JSON, samples, settings, hardware/browser/tool
versions, source commit and tracked-dirty status, and a Markdown report. It uses
independent per-metric medians, not best runs, and rejects comparisons with
different page sets, run counts, machines, browser or Lighthouse versions. Review
network settings, concurrent machine load and source differences too. Cold
browser caches do not reset OS/DNS/CDN caches; run-to-run variation remains.

CI measures the same seven pages and retains a `mobile-performance-report`
artifact for 30 days. Existing guide performance budgets remain ≥85; accessibility
and SEO budgets are ≥95 on all seven pages. Homepage/hub performance is initially
reporting-only until we calibrate their hosted-runner baselines, avoiding a new,
uncalibrated release gate. Their measured results are always retained.
These are checks, not proof of complete accessibility, Google indexing or ranking
gains. Existing playback/layout checks remain in Chromium plus the separate
desktop/mobile-size Firefox and WebKit matrix.

## Measurement tracks: do not mix the outcomes

| Track | Capture | Follow-up |
|---|---|---|
| Lab performance | LCP, FCP, TBT, CLS, bytes and performance/accessibility/SEO scores | Before/after the same build change; every CI run |
| Search visibility | Search Console/Bing indexed canonicals, queries, impressions, clicks and CTR | Export a pre-launch period; compare matched 28-day windows after deployment, noting reporting lag and other changes |
| Real-user experience | Search Console Core Web Vitals or public CrUX data if traffic is sufficient | Review after the rolling field-data window refreshes; absent data is not a passing score |
| AI recommendations | Repeat accepted baseline prompts by surface/cohort; record mentions, recommendations and citations | Existing 7/14/30-day protocol; match models, account state, locale and search settings and record differences |

No analytics, telemetry, third-party measurement tags or identifiers are added.
Search-console exports and AI captures need account access or user-provided files.
API responses are not interchangeable with consumer ChatGPT/Claude/Google/
Perplexity sessions. Lab gains do not imply ranking or recommendation gains.
This change does not submit indexing requests.

## Asset maintenance

`python3 scripts/prepare_performance_assets.py` regenerates responsive images
using macOS `sips` and `cwebp`. Add `--fonts` only when intentionally refreshing
the existing licensed Latin WOFF2 subsets; other scripts use system fallbacks.
Generated assets are committed, so deployment does not need image tools or
font-service network access. Visually inspect new variants and run
`npm run check:cross-browser` after regenerating.
