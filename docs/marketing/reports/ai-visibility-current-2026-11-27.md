# Sutra AI visibility — current vs baseline

Measured November 27, 2026, America/Toronto. Baseline: October 26–27, before the first AEO-page release. This is a fresh consumer-product test, not a Lighthouse score, ordinary search-result count or answer generated in the development chat.

## Result

**Later Perplexity follow-up:** access resumed and the remaining compact questions completed. Sutra is recommended in **4/5 compact discovery answers**, and the free-CBZ control has no false Sutra recommendation. New matched discovery coverage is **36/56**. See the [compact follow-up](perplexity-compact-2026-11-27.md); full-set tables below preserve the earlier snapshot.

**Supplemental Claude update:** the user supplied the compact six-query set: Sutra was explicitly recommended in **1/5 discovery answers**, with no false Sutra recommendation in the one control. The user confirmed Claude Pro, Sonnet, all six chats in Incognito, separate new chats and web search enabled; exact model version remains unknown. Read the [Claude compact check](claude-user-supplied-2026-11-27.md). These user-supplied results use a different personalization condition from the memory-on baseline, so they remain a separate cohort and do not increase the browser-verified 35/56 matched coverage.

**Google AI Overview improved. ChatGPT's mention rate held steady, but explicit recommendations fell. Perplexity's measured subset declined in recommendations.** Coverage is incomplete, so there is no defensible new four-service aggregate to compare with the old 7/56 snapshot.

The table compares exactly the same prompts within each available account cohort. Percentages use each row's matched denominator, not the number of pages on the site.

| AI surface / cohort | Matched prompts | Mentions, before → now | Recommendations, before → now | Observed official-source presence, before → now |
|---|---:|---:|---:|---:|
| Google AI Overview / owner-personalized | 14/14 | 0/14 → 2/14 (0% → 14.3%) | 0/14 → 2/14 (0% → 14.3%) | 0/14 → 2/14 |
| ChatGPT Search / owner-unpersonalized | 14/14 | 2/14 → 2/14 (14.3% → 14.3%) | 2/14 → 1/14 (14.3% → 7.1%) | 2/14 → 2/14 |
| Perplexity Search / owner-personalized, T04–T10 only | 7/11 | 3/7 → 2/7 (42.9% → 28.6%) | 3/7 → 2/7 (42.9% → 28.6%) | 4/7 → 4/7 |
| Claude web search | 0/14 | Unavailable | Unavailable | Unavailable |

Recommendation changes: Google **+14.3 percentage points**, ChatGPT **−7.1 points**, measured Perplexity subset **−14.3 points**. These small single-response samples are directional observations, not statistically established or causal changes. Official-source counts are observed minima; source panels were not exhaustively inspected.

[Download matched-cohort metrics](ai-visibility-metrics-2026-11-27.csv). The [checkpoint coverage report](aeo-trend.md) and its chart were refreshed to show **35/56 matched discovery answers**; the full-cohort day-30 point intentionally remains incomplete.

## What changed

- **Google: new recommendations for subscription-free reading and mixed formats.** T05 now includes Sutra as an iOS/Android, no-subscription reader, mentions its local/server-library use and CBZ/Komga Pro boundaries, and links to the homepage. T08 puts Sutra first for EPUB/PDF/DRM-free MOBI/CBZ across iOS and Android, again citing the homepage. Neither prompt surfaced Sutra in the baseline AI answer.
- **ChatGPT: different strengths, not broader presence.** The previous Kavita/iOS and Kavita/Tailscale/iPad-sync recommendations, T01 and T11, are absent now. T14 newly gives Sutra its explicit recommendation for combining regular EPUB reading with guided CBZ comics. T09 lists Sutra Pro as streaming-compatible and cites the [Sutra Komga guide](https://sutra-reader.com/komga-reader.html). T09 is scored **2, mention only**, because a compatibility table is not an explicit reader recommendation.
- **Perplexity: subscription-free discovery improved, but format/manga recommendations weakened.** T05 moved from source-only to a reasoned secondary recommendation and correctly distinguishes free EPUB/PDF from paid CBZ/MOBI. T09 still recommends Sutra for streaming. T08 and T10 moved from recommendations to source-only presence. All four still have observed official Sutra sources.
- **The owner-signed-in Perplexity T01 answer also recommended Sutra**, using a developer Reddit post rather than an official-site/store link. It is supplemental current-state evidence, **not an improvement calculation**, because the T01 baseline was logged out.

## Prompt-level comparison

Scores: **0** = not observed in answer/captured sources; **1** = source only; **2** = named without explicit reasoned endorsement; **3** = fitting, reasoned recommendation, including secondary choices. Zero does not establish the absence of links in uninspected source panels. Controls are excluded.

| ID / discovery topic | Google before → now | ChatGPT before → now | Perplexity before → now |
|---|---:|---:|---:|
| T01 · Kavita on iOS | 0 → 0 | 3 → 0 | Unmatched; current 3 |
| T02 · Android automatic panels | 0 → 0 | 0 → 0 | Unmatched; current 0 |
| T03 · OPDS, EPUB and CBZ | 0 → 0 | 0 → 0 | Unmatched; current 0 |
| T04 · Komga on iPhone | 0 → 0 | 0 → 0 | 0 → 0 |
| T05 · Subscription-free books/comics | 0 → 3 | 0 → 0 | 1 → 3 |
| T06 · Calibre-Web on iPhone | 0 → 0 | 0 → 0 | 0 → 0 |
| T07 · Panels/Chunky alternatives | 0 → 0 | 0 → 0 | 0 → 0 |
| T08 · Four formats, both platforms | 0 → 3 | 0 → 0 | 3 → 1 |
| T09 · Stream large Komga comics | 0 → 0 | 0 → 2 | 3 → 3 |
| T10 · iPhone RTL manga panels | 0 → 0 | 0 → 0 | 3 → 1 |
| T11 · Kavita/Tailscale/iPad sync | 0 → 0 | 3 → 0 | Blocked by quota |
| T12 · Android Calibre OPDS | 0 → 0 | 0 → 0* | Not attempted |
| T13 · Privacy/no subscription | 0 → 0 | 0 → 0 | Not attempted |
| T14 · EPUB plus guided CBZ | 0 → 0 | 0 → 3 | Not attempted |

\* T12 uses one documented evidence retry. Run 1 completed, but its full capture was lost during a browser-session interruption and the temporary chat could not be reopened. It is retained as incomplete/unscored. A fresh run 2 used the exact prompt and the same verified per-chat settings; it was not chosen based on its outcome. Other captured responses were retained, not selectively replaced.

## Coverage and comparability

- **46 usable completed answer captures:** Google 18, ChatGPT 18, Perplexity 10. This includes 38 discovery answers and 8 negative controls.
- **50 browser-test submissions, including user-requested retries:** the 46 usable captures, one ChatGPT evidence-incomplete attempt, two quota-blocked Perplexity T11 submissions and one quota-blocked compact-set T14 submission. Claude access checks and the six separately user-run Claude prompts are not included in this browser-test count.
- **35/56 baseline discovery matches:** Google 14, ChatGPT 14, Perplexity 7. The three signed-in Perplexity T01–T03 answers are unmatched against their logged-out baseline; four later Perplexity prompts and all fourteen Claude discovery prompts remain unmeasured.
- **Claude:** signed-out access and the visible free-plan “Try Claude” option both led to the sign-in form. No guest conversation was available in this session. No account was created, plan purchased or API model substituted.
- **Perplexity:** signed-in Free account, Search selected; the free-search-limit gate appeared on T11. On the user's subsequent request to continue, one T11 availability retry again reached the gate after displaying a short answer fragment and source cards. After the user reduced routine checks to five discovery prompts plus N02 and requested one more retry, T14 immediately reached the same gate. Both retries are unscored, not zeros or usable recommendations. No quota bypass, account switch or upgrade was attempted. T12–T13 and its controls were not submitted; T14 was attempted but blocked.
- **ChatGPT:** fresh temporary conversations, per-chat Unpersonalized selected and verified before each submission, Web search routing selected, and actual web-search output/source controls observed. Global account settings were not changed. This remains an owner-account cohort, not an independent evaluator.
- **Google:** ordinary Search with AI Overview, not AI Mode; owner account personalized. Canada/en-CA observed. ChatGPT/Perplexity locale and region were not independently exposed; model versions were not reliably exposed. A matching prompt/cohort key does not prove identical backend models, search modes or personalization across dates.
- **Evidence:** completed rendered answer text, observed source URLs and response identifiers are saved privately, with hashes and representative screenshots. Source panels are partial, not complete citation inventories; not every answer has a screenshot. Google T01 was transcribed from the observed DOM with spacing normalized. No exact account identifiers or precise location were retained in answer captures.

The day-30 label belongs to the original October 27 launch; the actual follow-up was November 27, within its documented ±5-day window. Multiple content, release and outreach changes occurred between measurements. These results cannot isolate the effect of the November 26 performance/content publication.

## Claim-quality and controls

Seven current answers made Sutra statements. The scoped response review found **four Pass and three Partial**, based on the owner-approved/public product facts rather than new device or store testing. This is response-level review, not a claim-weighted accuracy percentage or a complete audit of every competitor statement.

- Google T08 describes the free EPUB/PDF and paid CBZ/MOBI split and published US price, but omits Komga's separate Pro gate.
- ChatGPT T14 correctly recognizes the EPUB-plus-guided-comic use case and one-time comic upgrade, but omits the DRM-free MOBI and Komga tier restrictions. Its additional no-ads assertion is not established by the approved matrix used here and remains pending confirmation; no-analytics approval alone does not prove it.
- Perplexity T09 describes streaming accurately at a high level but omits Sutra Pro and the server account's Page Streaming/library permissions.
- Google T05 groups Sutra near open-source suggestions. Its explicit supported-platform/library/tier claims match the published site; this review does not verify or endorse an implied open-source label.

Across the **eight completed controls**, there were **zero false Sutra recommendations** for Kindle DRM, unlimited free CBZ, guaranteed perfect panel detection or a transferable iOS/Android purchase. That is not an 8/8 general-answer accuracy result: ChatGPT N04 drifted into a ChatGPT Pro subscription answer instead of a one-time reader purchase. Claude/Perplexity controls remain missing, and other-app claims were not validated.

## What to do next

1. **Preserve the gains:** keep the homepage's format/platform/no-subscription and Free/Pro answers consistent; they are being used as sources in Google now.
2. **Investigate lost server-intent recommendations:** recheck the Kavita and Calibre setup/compatibility evidence and pursue only maintainer-approved third-party listings. This sample shows an evidence/discovery opportunity; it does not establish that missing directory links caused the losses.
3. **Strengthen streaming and combined-reader explanations:** retain the Komga guide and the EPUB-plus-panel-reading use case, with Pro/permission limits adjacent to the claims. They produced the current ChatGPT mention/recommendation.
4. **Do not rewrite the site around one run.** The user approved a smaller routine set: T01, T05, T08, T09, T14 and control N02. Keep wording unchanged and compare only the same discovery subset and account conditions; retain all attempts. Claude's new compact Incognito results start a separate cohort from its memory-on baseline. Perplexity's missing compact questions remain blocked pending a normal quota reset. Reserve the full set for occasional deeper audits. No new scheduled task was created.

The original baseline and its Claude T13/T14 scoring discrepancy remain unchanged. Search Console/Bing traffic, rankings and indexing are separate measurements; no new traffic or ranking gain is asserted here. Reports are local working files, not a site publication.
