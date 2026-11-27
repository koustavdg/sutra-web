# Sutra SEO/AEO after-report — November 26, 2026

## Bottom line

The approved update is live. The core technical checks pass, product facts are consistent across the checked pages, and the controlled before/after lab measurements show a faster, lighter homepage. Search traffic, rankings and AI recommendation gains are **not measured yet**. Those outcomes must not be inferred from Lighthouse scores or successful deployment.

Release: `98bd783f710571e7bbe78bdfb9dd68ad504185bb`. Live checks began at 2026-11-27 04:47 UTC, November 26 in America/Toronto. This is a post-publication snapshot, not a full post-release search reporting period.

- [Deployment — success](https://github.com/koustavdg/sutra-web/actions/runs/45927032300)
- [Site quality — build/check and cross-browser jobs both succeeded](https://github.com/koustavdg/sutra-web/actions/runs/45927032360)
- [Visibility trend and measurement gaps](visibility-trend-2026-11-26.md)

## Published-site checks

Fetched ordinary public URLs, not preview URLs or cache-busting query variants. Parsed the raw HTML with the repository's HTML parser; checked sitemap-page titles, descriptions, canonicals, H1 counts, robots directives, JSON-LD syntax and links to other sitemap pages/anchors.

| Check | Observed result |
|---|---|
| Sitemap HTML URLs | 16/16 returned HTTP 200 |
| Unique titles and meta descriptions | 16/16; no duplicates among canonical sitemap pages |
| Canonicals | 16/16 match the sitemap URL |
| H1 | Exactly one on each of the 16 pages |
| Indexability directives | No detected meta or HTTP `noindex` on the sitemap pages |
| Internal page links/anchors | 333 checked; no detected broken targets within the sitemap-page set |
| JSON-LD | All encountered blocks parse; this is not full schema eligibility validation |
| Runtime Google Fonts stylesheet | None detected on any of the 16 pages |
| Local font / responsive image | Sample WOFF2 and WebP returned 200 with matching content types |
| Crawl files | `robots.txt`, `sitemap.xml`, `llms.txt`, `llms-full.txt` accessible |
| Crawl policy | Wildcard, Googlebot, Bingbot and named AI crawler groups allow `/` |
| HTTP and www aliases | Requests resolve to the HTTPS non-www homepage |
| `/index.html` alias | Still returns 200; its canonical points to `/` |
| IndexNow | Deployment log records acceptance of 16 canonical URLs, HTTP 200, at 2026-11-27 02:18:43 UTC |
| IndexNow verification file | Returned 200; content matches the public key |

Acceptance by IndexNow is notification acceptance, not confirmation of crawling, indexing, rankings or appearance in Bing's reporting dashboard. An HTTP fetch and an allowing robots policy also do not prove successful access by every real crawler.

### Canonical page inventory

All rows returned 200, had a matching canonical and one H1. Meta-description lengths are descriptive, not hard ranking thresholds.

| Path | Description characters |
|---|---:|
| `/` | 147 |
| `/help.html` | 136 |
| `/iphone-duo.html` | 162 |
| `/changelog.html` | 90 |
| `/feedback.html` | 124 |
| `/privacy.html` | 123 |
| `/drm-free.html` | 134 |
| `/about.html` | 129 |
| `/calibre-reader.html` | 137 |
| `/comic-panel-reader.html` | 143 |
| `/kavita-reader.html` | 135 |
| `/komga-reader.html` | 147 |
| `/opds-reader.html` | 141 |
| `/compare-readers.html` | 140 |
| `/sutra-vs-readest.html` | 143 |
| `/sutra-vs-panels.html` | 147 |

## AEO/content verification

The homepage, Help, Panels comparison and both LLM files consistently distinguish shipped landscape two-page layouts on iPad/Android tablets from comic-spread detection and page-pairing improvements still in development. The homepage and both LLM files identify current releases as iOS 2.5.0 and Android 1.3.0. Version summaries are not required on every guide/comparison page.

The homepage contains SoftwareApplication/Offer and Organization data; Help contains HowTo and FAQ data; the Duo page contains breadcrumb/FAQ data; comparison pages contain WebPage/breadcrumb data, with ItemList on the hub. Five server/reading-style guides have no JSON-LD blocks; their plain-text answers and internal links remain available. More markup is not automatically a higher-priority task than useful content and evidence.

`llms.txt` and `llms-full.txt` are consistent supporting summaries, not a guaranteed AI-discovery channel. Google states that normal SEO practices apply to its AI features and that special AI files or schema are not required. See [Google's AI features guidance](https://developers.google.com/search/docs/appearance/ai-features).

## Performance: keep three measurement contexts separate

### 1. Controlled local before/after

Three cold-cache mobile runs per page on the same local machine/toolchain. These are the valid paired observations for this release, documented in [the original performance report](../../performance/2026-11-26.md).

| Page | Performance before → after | LCP seconds before → after | Transfer KiB before → after |
|---|---:|---:|---:|
| Home | 75 → 89 | 4.79 → 3.47 | 952.6 → 620.2 |
| Comparison hub | 91 → 99 | 2.83 → 1.80 | 195.9 → 136.2 |
| Kavita | 92 → 99 | 2.71 → 2.11 | 213.2 → 186.5 |
| Komga | 92 → 99 | 2.70 → 2.10 | 213.2 → 186.5 |
| Panel comics | 92 → 99 | 2.79 → 1.95 | 207.4 → 147.3 |
| OPDS | 99 → 100 | 1.60 → 1.73 | 191.3 → 164.6 |
| Calibre | 95 → 100 | 2.37 → 1.73 | 191.6 → 164.9 |

Homepage LCP fell about 28%; transferred bytes fell about 35%. Not every metric improved: OPDS LCP rose 0.13 seconds, and the hub had small TBT/CLS increases. All seven pages scored 100 in Lighthouse SEO/accessibility before and after, so those scores did not improve.

### 2. Hosted CI verification

Site quality run 45927032360 measured the built artifact on a Linux runner at localhost, not the public CDN. Three-run medians:

| Page | Performance | LCP seconds | CLS | Transfer KiB |
|---|---:|---:|---:|---:|
| Home | 89 | 3.53 | 0.003 | 648.0 |
| Comparison hub | 100 | 1.80 | 0.002 | 136.2 |
| Kavita | 99 | 2.10 | 0.002 | 186.6 |
| Komga | 99 | 2.10 | 0.002 | 186.6 |
| Panel comics | 99 | 1.95 | 0.002 | 147.3 |
| OPDS | 100 | 1.80 | 0.002 | 164.6 |
| Calibre | 100 | 1.80 | 0.002 | 164.9 |

All seven had TBT 0 ms, accessibility 100 and SEO 100. This is a separate environment, not another paired improvement calculation. The `mobile-performance-report` CI artifact has a 30-day retention window; a local copy was retrieved under `output/performance/2026-11-26-hosted-ci/`.

### 3. Public-site mobile lab snapshot

Completed 21 cold-cache Lighthouse runs against the ordinary public URLs: three per page, with independent per-metric medians. Captured November 27, approximately 04:47–04:52 UTC, using Lighthouse 13.5.0 and Chromium 156 on the local Intel Mac. Results and raw reports are retained under `output/performance/2026-11-26-live-after/`.

| Page | Performance | LCP seconds | CLS | Transfer KiB |
|---|---:|---:|---:|---:|
| Home | 98 | 2.23 | 0.036 | 1341.1 |
| Comparison hub | 99 | 1.61 | 0.043 | 135.2 |
| Kavita | 100 | 1.60 | 0.001 | 170.2 |
| Komga | 100 | 1.61 | 0.001 | 186.3 |
| Panel comics | 100 | 1.60 | 0.001 | 332.7 |
| OPDS | 100 | 1.36 | 0.001 | 148.6 |
| Calibre | 100 | 1.36 | 0.001 | 148.7 |

All seven had median TBT 0 ms, accessibility 100 and SEO 100. These results establish a live-after baseline, not a comparable delta against localhost, CI or a previous single-run live audit. No field Core Web Vitals claim is made.

The public homepage's transferred total includes Android comic, auto-scroll and preview MP4 data; these requests account for much of its difference from CI. Totals also vary between runs. Do not apply the controlled local 35% byte reduction to this live snapshot or mistake the Lighthouse transfer total for the initial HTML/image payload. This is a useful media-loading investigation target, not a demonstrated playback regression.

## Remaining priorities

1. **Finish outcome measurement.** Restore console access or supply exports, inspect selected canonicals/indexing for home, guides and comparisons, then repeat the frozen AI prompts. This is the main gap in the visibility report, not another schema tag.
2. **Continue homepage performance work only against measured bottlenecks.** The controlled/CI homepage LCP is still around 3.5 seconds despite the improvement. The live audit also transfers Android demo-video data, with variable totals across runs. Inspect the media-request lifecycle before changing it; the bytes audit alone does not prove an offscreen autoplay bug. Use the new report loop and field data when available; preserve video fallback/reduced-motion behavior.
3. **Consider host-level `/index.html` → `/` redirection if supported.** The canonical is already correct, so this is cleanup, not evidence of a duplicate-content penalty. Do not give the alias a different title to hide duplication. [Google canonicalization guidance](https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls) treats redirects and canonicals as consolidation signals.
4. **Convert accepted outreach into verified public evidence.** calibre merged the PR, but its current public FAQ lacks Sutra. Wait for upstream publication, then verify the actual link. Komga/Awesome OPDS remain pending; respect Kavita's decision.
5. **Keep release facts current.** Update the shared product facts and dated comparison evidence when TTS, pronunciation packs, KOSync/annotation sync or CBR/RAR actually ship. Do not promote development items into current capability claims early.
6. **Optional copy polish.** The changelog description is 90 characters; it could explain the two-platform release history more clearly. Length alone is not a failure or a reason for padding.

## Scope and limits

This pass checks public technical signals and published facts, not full search-engine indexing, exhaustive accessibility, real-device autoplay, all outbound links, all image assets, rankings or citations. No tracking was added. No indexing submissions, external messages, source/workflow changes, commit or publication were initiated by this reporting pass.
