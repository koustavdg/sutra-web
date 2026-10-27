# P0 publication and product-QA gate

Owner-attested support/tier facts are in `capability-matrix.md`. On October 27, 2026, Koustav confirmed completion of the six requested flows and confirmed the panel clip is current and cleared for publication. Device versions, server versions, detailed results, and individual evidence references were not provided; do not infer them. Do not place server URLs, credentials, API keys, account names, or private-library contents in captures.

## iOS and Android end-to-end flows

Record device/app version, server version/configuration, date, result, and a sanitized evidence reference for each row. Koustav signs off on all six platform/theme flows.

| Theme | Platform | Flow to verify | Status |
|---|---|---|---|
| Kavita | iOS | Connect using a redacted personal OPDS URL; open free EPUB/PDF; confirm observed progress behavior without asserting unverified units | Completed; owner attested |
| Kavita | Android | Connect using a redacted personal OPDS URL; open free EPUB/PDF; confirm observed progress behavior without asserting unverified units | Completed; owner attested |
| Komga | iOS | Pro-gated Komga connection; stream with Page Streaming permission; verify download fallback without permission | Completed; owner attested |
| Komga | Android | Pro-gated Komga connection; stream with Page Streaming permission; verify download fallback without permission | Completed; owner attested |
| Panel reading | iOS | Toggle full-page/panel mode; test right-to-left order, a page without detected panels, and current preview/Pro boundary | Completed; owner attested |
| Panel reading | Android | Toggle full-page/panel mode; test right-to-left order, a page without detected panels, and current preview/Pro boundary | Completed; owner attested |

## Media sign-off

- [x] Confirm the included panel-reading clip depicts current publicly released behavior and Sutra has permission to publish its comic imagery/audio-derived video. Owner confirmed October 27, 2026.
- [ ] Confirm the sanitized connection screenshot contains no live URL, token, credential, account, or private-library information.
- [ ] Confirm the current store destinations identify the intended Sutra apps (identity was checked October 27, 2026; feature behavior and prices were not validated by that check).

## Publication gate

- [x] Local public-only build, canonical/meta/H1, internal-link, robots, sitemap, matrix-ID, media-caption/transcript, and privacy-artifact checks pass.
- [ ] GitHub Actions browser tests pass at 390px and 1440px, including keyboard disclosure and serious/critical axe checks.
- [x] Six platform/theme app flows above are signed off by Koustav (owner attestation; individual evidence details not supplied).
- [ ] Live crawl status/redirect/headers and Search Console/Bing access handoff are recorded after production release.
- [ ] Google Rich Results Test is run against the live page; a documented ineligible result is acceptable if genuine rating/offer requirements are absent.
- [ ] After pre-publication checks: publish the built artifact from `main`, then run live checks and record sitemap submission/indexing evidence.

Do not infer approval from the existing public copy, screenshots, store descriptions, or this checklist. Any missing evidence blocks only the affected claim/page; indexing and AI recommendations remain observed outcomes, never guarantees.
