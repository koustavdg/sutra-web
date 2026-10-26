# Baseline status — October 26, 2026

Campaign baseline-2026-10. **Not completed. No recommendation answers captured or scored.**

## Access observations

Observed using the Codex in-app browser, not the developer search connector. These are access probes, not prompt attempts and not a measured recommendation baseline.

| Surface | Observed state | Baseline consequence |
|---|---|---|
| ChatGPT Search | Logged out; composer available. Web search checkbox remained off when selected in the attachment menu. | Search-enabled protocol cannot currently be confirmed. Needs an eligible search-enabled session; no no-search answer will be substituted. |
| Claude | claude.ai redirects to sign-in. | Requires owner/evaluator to provide a signed-in session. |
| Google | Canada shown; account signed in; AI Mode link visible. | Owner account may personalize results. Await decision on using that account vs independent evaluator. No Google result collected. |
| Perplexity | Logged out; blank new composer; Search checked. | Ready for unseeded collection, with actual region/model recorded as unknown if not disclosed. |

Prompts and CSV schemas are prepared. Capability approvals are pending before eligibility/accuracy adjudication. Keep actual capture separate from scoring; never invent or extrapolate answers for inaccessible surfaces.

## Next actions

1. Koustav reviews capability-matrix.md and supplies corrections/approval.
2. Resolve account/evaluator availability for ChatGPT and Claude and the Google personalization choice. No passwords or keys in files/chat.
3. Execute prompts.csv verbatim, in fresh conversations, across the available approved cohorts. Append only actual attempts; store complete raw answers privately with hashes.
4. Report missing surfaces explicitly. Do not mark #7 done or publish AEO changes while the baseline gate is unmet unless the owner explicitly changes that gate.

## Scope completed here

- Draft content/product.json (52 unverified claims; no approved numeric offers).
- Readable matrix with source references, discrepancy list and owner review questions.
- Frozen prompt file, test protocol, results/claim/evidence CSV schemas.
- No public HTML edits, no site build, no commit/push/deploy, no issue closure.

The existing deployment uploads the repository root: keep these internal working files off main until the public artifact is explicitly constrained in #6/#18.
