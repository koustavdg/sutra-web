# Recommendation-test protocol v1

Prepared 2026-10-26 for #7. Campaign: baseline-2026-10. This is a prepared protocol, not a completed baseline.

## Frozen prompts

Use prompts.csv verbatim: 14 eligible-candidate queries and 4 negative controls. Parenthetical expected answers are evaluator notes and must NEVER be included in prompts. Prompts are frozen for this campaign; changes start a new version/cohort. Eligibility remains provisional until Koustav approves capability-matrix.md.

## Surfaces and sample size

ChatGPT Search, Claude web search, Google Search AI Overview (record AI Mode separately if used), Perplexity Search. Minimum one run per prompt per primary surface: 72 attempts; target three: 216. Additional Google AI Mode tests are a separate cohort, not a replacement chosen after seeing results.

For each run, open a genuinely fresh conversation/search. Do not mention Sutra, owning the app, AEO, or expected answers. Do not prime by opening Sutra sources in the same conversation. Record sign-in/plan, personalization limitations, displayed model version (unknown if hidden), search enabled and actual search evidence, locale and region. Region must be observed, not assumed from the host clock. Target Canada/en-CA; record actual values and isolate differences.

Use a neutral evaluator/session where available. This development chat is ineligible as a response source. A signed-in owner's history is a disclosed limitation, not an independent neutral evaluator. Never change account memory/privacy settings as part of a run. Never create accounts, purchase plans or bypass challenges to obtain results.

## Capture and log

1. Select the next prompt in ID order; record surface and run ID before submission. A run is submitted only once; if it fails, retain status and give any retry a new run ID.
2. Wait for generation to finish and retain full verbatim answer, source links and screenshots. Avoid copying irrelevant account/profile details. Assign an evidence ID and store raw material privately outside any Pages artifact. Record its path and SHA-256 in evidence-manifest.csv after actual capture.
3. Append actual attempts to recommendation-tests.csv. Never prefill fabricated runs or scores for unopened prompts. Access checks are logged in baseline-status.md, not counted as 18 attempted prompts.
4. Track completed, no_ai_answer, search_unavailable, access_blocked, failed and incomplete separately. A Google ordinary SERP without an AI answer is no_ai_answer; retain ordinary search evidence separately. Report this coverage explicitly.
5. Score visibility only for a completed AI answer: 3 = concrete fitting recommendation with a reason (including secondary recommendations); 2 = named without reasoned endorsement; 1 = only linked/cited; 0 = absent. Record rank only for an explicit ordered recommendation list, otherwise blank.
6. Controls are excluded from recommendation-rate denominator. No Sutra statement means accuracy N/A, never Pass. Each Sutra statement gets its own row in recommendation-claims.csv mapped to an approved product claim ID. Pass = accurate including necessary restrictions; Partial = material caveat missing but no false statement; Fail = false claim. Unapproved ground truth stays unscored/pending_owner_review.
7. For response-level accuracy use the worst scored claim (Fail > Partial > Pass), with pending claims explicitly noted. Do not conceal a wrong tier behind correct unrelated facts.

## Reporting

Per surface and checkpoint: planned count, attempted count, completed answers, failures/unavailable/no-AI coverage, eligible completed answers, recommendations (3), mentions (2+3), recommendation rate, mention rate, and claim-level Pass/Partial/Fail counts. Accuracy = Pass / all evaluated Sutra statements; report pending claims separately. No statements => N/A. Preserve denominators/sample sizes. Do not pool different models, search modes or regions without showing cohorts. Keep negative-control accuracy separate.

The baseline must finish before public AEO metadata, copy, robots or landing changes. If a surface cannot be measured, disclose the gap and obtain an explicit owner decision before treating the baseline gate as satisfied. Baseline preparation is not baseline completion.

Postlaunch follow-up belongs to #17: day 7/14/30 from actual first P0 launch, using the same prompts/surfaces and reporting version/indexing changes. No recurring automation is created by this protocol.

## Private evidence and deployment

The existing Pages workflow uploads the repo root. Do not commit/push internal evidence or these working docs to main until #6/#18 excludes them from the public artifact. No production build/deploy is part of this preparation step. No IPs, emails, tokens, session cookies or live server credentials in evidence exports.
