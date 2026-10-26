# Capability matrix — owner review

Prepared October 26, 2026 from repository snapshot b92c7a7 for issue #5.

**Draft: none of these rows is approved.** Published copy is evidence of what the site says, not proof of current app behavior. The machine-readable source is [content/product.json](../../content/product.json). Every claim has a separate platform row; null release/version/sync fields mean unknown, not universal support.

Koustav can approve the ordinary rows together and correct exceptions by claim ID. Record his exact confirmation, review date, current app versions, and evidence per affected row before changing its status to verified. False proposed support is a draft unsupported claim and also needs approval. No numeric prices are approved.

| Claim ID | Proposed capability | Platform | Proposed tier | Conditions / boundary | Source |
|---|---|---|---|---|---|
| epub-pdf-ios | EPUB/PDF reading | ios | free | Local file or supported library | [copy](https://sutra-reader.com/index.html#compare) |
| cbz-full-ios | Full CBZ reading | ios | pro | Local file or supported library | [copy](https://sutra-reader.com/index.html#compare) |
| mobi-full-ios | Full DRM-free MOBI reading | ios | pro | Local file or supported library | [copy](https://sutra-reader.com/help.html#getting-started) |
| cbz-preview-ios | 7-page CBZ preview | ios | preview | Confirm preview scope and counting per platform | [copy](https://sutra-reader.com/index.html#features) |
| mobi-preview-ios | 7-page comic-shaped MOBI preview | ios | preview | Confirm which MOBI files qualify | [copy](https://sutra-reader.com/index.html#features) |
| local-import-ios | Local file import | ios | format-dependent | Device file picker/share sheet | [copy](https://sutra-reader.com/index.html#features) |
| kavita-catalog-ios | Kavita library connection | ios | free | Personal OPDS URL; API key must stay private | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| komga-catalog-ios | Komga library connection | ios | pro | Bare server URL and account credentials | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-ios | Calibre Content Server | ios | free | Reachable server; verify base/feed URL and authentication | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-web-ios | Calibre-Web | ios | free | Verify server version/auth/feed on each platform | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-web-automated-ios | Calibre-Web-Automated | ios | free | OPDS enabled, account permissions; separate login portal unsupported unless OPDS reachable | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| opds-ios | Generic OPDS catalog access | ios | free | Verify supported feed/auth types; file entitlement separate | [copy](https://sutra-reader.com/index.html#compare) |
| webdav-ios | Read-only WebDAV library | ios | free | Reachable server and credentials; verify certificate trust | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| panel-mode-ios | Automatic Panel Mode | ios | free | Supported comic formats; entitlement still applies to full CBZ/MOBI | [copy](https://sutra-reader.com/index.html#compare) |
| rtl-ios | Right-to-left manga panel ordering | ios | free | Supported comic layout; full-file entitlement separate | [copy](https://sutra-reader.com/index.html#compare) |
| kavita-sync-ios | Kavita reading-progress sync | ios | free | Confirm formats, progress units, read/write direction and conflict handling | [copy](https://sutra-reader.com/index.html#features) |
| komga-sync-ios | Komga reading-progress sync | ios | pro | Confirm formats, progress units, read/write direction and conflict handling | [copy](https://sutra-reader.com/index.html#compare) |
| kavita-stream-ios | Kavita CBZ page streaming | ios | pro | Supported server endpoints/version; confirm fallback and preview | [copy](https://sutra-reader.com/help.html#getting-started) |
| komga-stream-ios | Komga CBZ page streaming | ios | pro | Page Streaming + library permissions; verify full-download fallback | [copy](https://sutra-reader.com/help.html#getting-started) |
| offline-ios | Offline reading | ios | format-dependent | Complete local/downloaded file; current tier entitlement | [copy](https://sutra-reader.com/changelog.html) |
| pro-purchase-ios | One-time Pro purchase per platform | ios | pro | Separate iOS and Android purchases; verify restore scope | [copy](https://sutra-reader.com/index.html#compare) |
| privacy-ios | No app analytics/tracking | ios | all | No claim of zero network traffic; servers/catalogs/store services exchange data | [copy](https://sutra-reader.com/privacy.html) |
| epub-pdf-android | EPUB/PDF reading | android | free | Local file or supported library | [copy](https://sutra-reader.com/index.html#compare) |
| cbz-full-android | Full CBZ reading | android | pro | Local file or supported library | [copy](https://sutra-reader.com/index.html#compare) |
| mobi-full-android | Full DRM-free MOBI reading | android | pro | Local file or supported library | [copy](https://sutra-reader.com/help.html#getting-started) |
| cbz-preview-android | 7-page CBZ preview | android | preview | Confirm preview scope and counting per platform | [copy](https://sutra-reader.com/index.html#features) |
| mobi-preview-android | 7-page comic-shaped MOBI preview | android | preview | Confirm which MOBI files qualify | [copy](https://sutra-reader.com/index.html#features) |
| local-import-android | Local file import | android | format-dependent | Device file picker/share sheet | [copy](https://sutra-reader.com/index.html#features) |
| kavita-catalog-android | Kavita library connection | android | free | Personal OPDS URL; API key must stay private | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| komga-catalog-android | Komga library connection | android | pro | Bare server URL and account credentials | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-android | Calibre Content Server | android | free | Reachable server; verify base/feed URL and authentication | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-web-android | Calibre-Web | android | free | Verify server version/auth/feed on each platform | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| calibre-web-automated-android | Calibre-Web-Automated | android | free | OPDS enabled, account permissions; separate login portal unsupported unless OPDS reachable | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| opds-android | Generic OPDS catalog access | android | free | Verify supported feed/auth types; file entitlement separate | [copy](https://sutra-reader.com/index.html#compare) |
| webdav-android | Read-only WebDAV library | android | free | Reachable server and credentials; verify certificate trust | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| panel-mode-android | Automatic Panel Mode | android | free | Supported comic formats; entitlement still applies to full CBZ/MOBI | [copy](https://sutra-reader.com/index.html#compare) |
| rtl-android | Right-to-left manga panel ordering | android | free | Supported comic layout; full-file entitlement separate | [copy](https://sutra-reader.com/index.html#compare) |
| kavita-sync-android | Kavita reading-progress sync | android | free | Confirm formats, progress units, read/write direction and conflict handling | [copy](https://sutra-reader.com/index.html#features) |
| komga-sync-android | Komga reading-progress sync | android | pro | Confirm formats, progress units, read/write direction and conflict handling | [copy](https://sutra-reader.com/index.html#compare) |
| kavita-stream-android | Kavita CBZ page streaming | android | pro | Supported server endpoints/version; confirm fallback and preview | [copy](https://sutra-reader.com/help.html#getting-started) |
| komga-stream-android | Komga CBZ page streaming | android | pro | Page Streaming + library permissions; verify full-download fallback | [copy](https://sutra-reader.com/help.html#getting-started) |
| offline-android | Offline reading | android | format-dependent | Complete local/downloaded file; current tier entitlement | [copy](https://sutra-reader.com/changelog.html) |
| pro-purchase-android | One-time Pro purchase per platform | android | pro | Separate iOS and Android purchases; verify restore scope | [copy](https://sutra-reader.com/index.html#compare) |
| privacy-android | No app analytics/tracking | android | all | No claim of zero network traffic; servers/catalogs/store services exchange data | [copy](https://sutra-reader.com/privacy.html) |
| icloud-ios | iCloud reading position/bookmarks/highlights | ios | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/index.html#features) |
| icloud-android | iCloud reading position/bookmarks/highlights — not supported | android | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/index.html#features) |
| export-android | Android data export | android | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/index.html#features) |
| eink-android | Dedicated e-ink mode | android | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/index.html#compare) |
| drm-ios | Direct DRM-protected Kindle purchases — not supported | ios | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/help.html#getting-started) |
| drm-android | Direct DRM-protected Kindle purchases — not supported | android | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/help.html#getting-started) |
| cbr-ios | CBR archives — not supported | ios | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/help.html#connect-a-server) |
| cbr-android | CBR archives — not supported | android | confirm | Confirm current platform behavior | [copy](https://sutra-reader.com/help.html#connect-a-server) |

## Decisions needed from Koustav

1. Are EPUB/PDF, ordinary Kavita/Calibre/OPDS/WebDAV access and Panel Mode/RTL free on both platforms, while full CBZ/MOBI and Komga need Pro? Confirm the two preview rules and how the seven pages are counted.
2. Is Kavita/Komga CBZ streaming available on both current releases? Is Pro required, can previews stream, and is full download the fallback when streaming is unavailable? Confirm minimum server versions if known.
3. For Kavita and Komga: which formats sync, in which directions, and in what unit (page/percentage/EPUB position)? Confirm iCloud scope on iOS, Android export scope, and whether any Android cloud/cross-platform sync exists.
4. Confirm current publicly released app versions and approved comic media, including Panel Mode formats (CBZ, scanned PDF, fixed-layout EPUB/MOBI), RTL ordering, local/offline operation and fallback on irregular artwork.

## Reconciliation list (public files untouched)

- Home description broadly says free and best; do not let this imply free full CBZ/Komga.
- Home feature card says streaming is iOS; Android 1.2.0 release block says streaming shipped. Reconcile from owner approval.
- Home compare introduction says same features despite platform-specific features.
- Help Kavita setup says page-accurate sync for all books; define EPUB position vs exact PDF/comic page.
- Help sync FAQ only mentions Kavita and iCloud; home mentions Komga too.
- Help has $6.99 without currency/region and home repeats a price; use nonnumeric storefront copy unless explicitly verified.
- Home calls page curl iOS-only, but Android 1.3.0 release notes document it. Current-copy review must preserve historical release truth.
- Help is not platform-scoped; verify iOS-specific network/Tailscale guidance before presenting it to Android users.

## Approval and change checklist

- [ ] Koustav confirms or corrects each proposed claim, including unsupported rows.
- [ ] App/server versions and format-specific sync boundaries recorded where relevant.
- [ ] Store identity/current listing reviewed; discrepancies recorded without external edits.
- [ ] Evidence covers streaming permissions, offline use and preview/Pro boundaries.
- [ ] Any edited matrix row triggers review of home metadata/features/pricing, Help, current privacy wording, landing content and structured data.
- [ ] Historical changelog remains a dated record; don't rewrite old releases as current parity claims.

No product approval has been inferred from issue descriptions or the reference plan.
