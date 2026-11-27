# Sutra visibility trend update — November 26, 2026

**Follow-up — November 27:** Fresh AI tests are now available in the [current AI visibility report](ai-visibility-current-2026-11-27.md). The AI-data gaps below describe the November 26 review, not the latest measurement. Search-console traffic data is still not updated by that AI test.

## Status

**Technical readiness improved; search and AI visibility change is not yet measurable from the available evidence.** Missing follow-up data is not zero visibility and is not evidence that performance is unchanged.

This review follows release `98bd783` on November 26, America/Toronto. Public checks occurred November 27 UTC. See the [SEO/AEO after-report](seo-aeo-after-2026-11-26.md) for the live audit and the [existing AI chart](aeo-trend.md) for the frozen baseline.

The new public mobile lab baseline is complete: homepage performance 98 and median LCP 2.23 seconds; the other six measured pages scored 99–100. All seven scored 100 in Lighthouse SEO/accessibility. These are technical lab observations, not a visibility trend or proof of search/AI gains.

## Search visibility

| Measure | Historical baseline | New observation | Trend |
|---|---:|---|---|
| Google clicks | 21 | Unavailable | Not calculable |
| Google impressions | 506 | Unavailable | Not calculable |
| Google CTR | 4.2% | Unavailable | Not calculable |
| Google average position | 6.7 | Unavailable | Not calculable |
| Google indexed canonical pages | Not recorded in baseline | Not retrieved | Not calculable |
| Bing clicks/impressions/CTR/position | Unavailable | Not retrieved | Not calculable |
| Bing AI citations / cited pages, if available | Not recorded | Not retrieved | Not calculable |
| Non-brand search visibility | Not computed | Not retrieved | Not calculable |

The Google baseline is the owner-domain property's manual snapshot for September 28–October 25, 2026, retrieved October 27: [baseline detail](google-baseline-2026-10-27.md). It includes subdomains, including possible newsletter traffic. It must not be compared with a new root-host-only cohort without reconstructing the baseline. No export-backed page/query breakdown is available here.

At this review, the browser's signed-in Google account could not access `sc-domain:sutra-reader.com`; Bing Webmaster Tools was signed out. No account identifiers are recorded in this report. These are access limitations in this session, not proof that the owner lacks a verified property.

## AI answer visibility

No completed matched day-7/day-14/day-30 follow-up CSVs were found in the existing report/evidence locations inspected. The recommendation ledger and chart therefore remain baseline-only. The original October 27 launch's day-30 target is November 26; it must not be relabelled as a completed test merely because a new release went live that day.

| Surface / accepted cohort | Baseline eligible answers | Baseline mentions | Baseline recommendations | Observed official-source answers | Matched follow-up |
|---|---:|---:|---:|---:|---|
| ChatGPT / owner-unpersonalized | 14 | 2 | 2 | 2 | Not captured |
| Claude / owner-personalized, exact | 4 | 1 | 1 | 1 | Not captured |
| Claude / owner-personalized, prefixed | 10 | 1 | 1 | 0 | Not captured |
| Google AI Overview / owner-personalized | 14 | 0 | 0 | 0 | Not captured |
| Perplexity / logged-out | 3 | 0 | 0 | 0 | Not captured |
| Perplexity / owner-personalized | 11 | 3 | 3 | 4 | Not captured |

The mixed-cohort descriptive total is 7/56 mentions, 7/56 recommendations and 7/56 observed official-source answers, each 12.5%. This is **not competitive share of voice**. Source presence is a recorded minimum, not complete inline-citation capture. Claude T13/T14 have an unresolved score-versus-narrative discrepancy and T13 has possible personalization contamination; the table retains the existing ledger rather than silently changing history. See [baseline caveats](aeo-baseline-citation-visibility.md).

No new trend line or claimed uplift is added without new observations. Tool-assisted search spot checks are not equivalent to the frozen consumer-product AI tests.

## Additional discovery evidence

Checked on November 26 America/Toronto. These observations do not establish referral traffic, ranking gains or AI citation gains.

| Channel | Current evidence | Classification |
|---|---|---|
| Search-tool retrieval | Returned Sutra's homepage, Help and OPDS guide for targeted `site:` queries | Some pages retrievable through this tool; not a Google/Bing indexing count or rank measurement |
| [calibre PR #3494](https://github.com/kovidgoyal/calibre/pull/3494) | Merged November 22, 2026, 04:09 UTC | Accepted contribution; not yet a verified public FAQ backlink |
| [calibre public FAQ](https://manual.calibre-ebook.com/faq.html) | Returned 200, but fetched HTML did not contain Sutra or sutra-reader.com | Publication pending/unverified; do not count as live |
| [Komga PR #256](https://github.com/gotson/komga-website/pull/256) | Open, no merge timestamp | Pending request, not a new backlink |
| [Awesome OPDS PR #22](https://github.com/opds-community/awesome-opds/pull/22) | Open, no merge timestamp | Pending request, not a new backlink |
| [Kavita PR #157](https://github.com/Kareadita/Wiki-Nextra/pull/157) | Closed, no merge timestamp | Not accepted; respect maintainer's no-more-client-listings decision |
| [DuoWorthy](https://duoworthy.com/apps/sutra) | Returned 200 and contained a Sutra site link | Verified live listing; no earlier matched backlink census, so net growth is unknown |
| [Made for Duo](https://madeforduo.app/app/sutra-ebook-comic-reader) | Direct HTTP request returned 403 | Unverified in this fetch; not proof the listing is absent |

This is a small known-prospect check, not an exhaustive backlink audit or referring-domain count. Historical submission records remain dated records; this table supplies the current follow-up state.

## Measurement loop

### Obtain the missing outcome data

1. In Search Console, use the verified property and Web search. Export the latest complete 28-day period plus the preceding 28 days, with exact dates and reporting lag. Retain daily totals and page/query/device/country breakdowns separately; do not sum unlike exports.
2. Preserve a domain-wide series for continuity with the October baseline. Create a separate `https://sutra-reader.com/` root-host page cohort to avoid attributing newsletter impressions to the main site. Track the five library/reading-style guides and the three comparison URLs separately.
3. Apply a documented, consistent brand filter. Query rows may be anonymized/omitted and do not necessarily sum to totals. Do not manufacture a non-brand total by subtraction from incomplete query data.
4. Export Bing's analogous reports separately. Capture sitemap processing, representative URL inspection/selected canonicals, and IndexNow reporting as distinct indexing diagnostics. If Bing exposes AI performance, retain its exact metric definitions and date range rather than combining them with manual prompt scores.
5. Repeat the 56 accepted discovery prompt/surface/cohort pairs plus the separate negative controls. Use fresh unseeded sessions, web search, exact submitted wording, the recorded account/search conditions, complete answer/source evidence and the same scoring. Do not seed Sutra into an unbranded prompt. Record model/search-mode changes and blocked/no-answer cases.

Raw account exports and AI captures belong outside the public repository. Only reviewed aggregate results and non-sensitive source links should enter reports. No analytics scripts or app telemetry are needed for this loop.

### Release-relative review windows

These are proposed manual checkpoints, not scheduled automations. Console lag may require retrieving them later.

| Review | Window / action | Interpretation |
|---|---|---|
| Now | Live technical snapshot and accepted October baseline | Completed for technical signals; outcomes unavailable |
| December 3 | Review November 27–December 3, when fully reported | First seven full post-release days; small/noisy sample |
| December 10 | Review November 27–December 10; repeat matched AI cohort if practicable | Directional two-week evidence, not causal attribution |
| December 24 | Compare November 27–December 24 with October 29–November 25 | Two complete 28-day windows; exclude November 26's partial release day |

For shorter comparisons, match weekdays and page/property filters. Keep the earlier October 27 launch and later content/outreach changes annotated; the site has had multiple interventions, so a simple before/after cannot isolate this release's effect. Google Search Console's Web totals include traffic from its AI features rather than providing this manual cohort's citation rate; see [Google's measurement guidance](https://developers.google.com/search/docs/appearance/ai-features#measuring-the-performance-of-your-site).

## Next report decision rules

- **Search:** report absolute changes in clicks/impressions, CTR in percentage points, and position with direction clarified. Use the same property/cohort/date definitions; do not compare local lab scores with search visibility.
- **AI:** compare matched cohorts and prompt counts; report raw numerators/denominators and claim accuracy. Preserve missing or contaminated tests. Keep partial coverage separate; only publish a full aggregate trend point after all 56 unique eligible matches pass review.
- **Links:** distinguish submitted, merged, published and actually linked. None is an endorsement or proof of SEO effect.
- **Performance:** retain the new public three-run snapshot as a separate baseline. Use the same machine/browser/Lighthouse/settings/hosting context for future paired runs. Field Core Web Vitals need field data.
- **Privacy:** sessions, conversions, installs attributed to the website and AI-referred sessions remain N/A in this no-tracking measurement scope.
