# Capability approval — October 26, 2026

Owner: Koustav. Evidence: direct user message in this task after review of the draft matrix pushed in commit a66715f.

## Exact confirmation

> Confirmed all suggestions
> iCloud iOS is free
> iCloud Android is not supported
> export android is free
> e-ink android is free
> drm ios is not supported
> drm android is not supported
> cbr ios is not supported
> cbr android is not supported

## Scope recorded

All 52 proposed support/tier rows are approved by owner attestation, with the eight explicit entries above applied. There are 47 supported rows and 5 unsupported rows. iCloud on iOS, Android export and Android e-ink are free. iCloud on Android, direct DRM-protected Kindle reading on either platform and CBR on either platform are unsupported.

This confirmation does not provide missing version numbers, format-specific sync granularity/direction, preview page-counting details, preview streaming behavior, media licenses, numeric storefront prices, device test results or independent listing verification. Those remain unknown and must not be inferred from broad approval. Published-copy links retain provenance but are not proof of device testing.

No website content has been changed or published by recording this approval. Issue #5 still has public-copy reconciliation and evidence work outstanding. The recommendation baseline remains incomplete.

## iPhone Duo — November 4, 2026

Owner: Koustav. Evidence: direct user answers in this task to the iPhone Duo questions in [iphone-duo-capability-draft.md](iphone-duo-capability-draft.md), drafted from the iOS 2.5.0 release notes at repository snapshot 1fb8050.

### Exact confirmation

> Comics on iPhone Duo (two-page facing pages and Panel Mode on the Duo displays): Free preview, full with Pro
> Two-page EPUB and PDF spreads on iPhone Duo: Free
> Fold-aware layout on iPhone Duo: Free
> Sutra 2.5.0 is the minimum version for iPhone Duo support: confirmed
> Features table iPhone Duo row: keep the check mark in the Free column
> Apply the iPhone Duo rows to content/product.json: yes; device details not needed

### Scope recorded

Five rows are added to `content/product.json` as owner-attested, all with `approved_at` 2026-11-04 and reviewer Koustav: `duo-two-page-ios` (free), `duo-comics-preview-ios` (preview), `duo-comics-full-ios` (pro), `duo-fold-layout-ios` (free), and `duo-min-version-ios` (2.5.0 minimum, not applicable tier).

Evidence is owner attestation only. No device test, app build, or store listing check was supplied, and `app_version` and `server_version` remain null. Release-note wording is not device QA. The Features table's Free column shows a check for the iPhone Duo row, even though comics are preview-only in Free; this was an explicit owner decision.
