# Sutra Web — CLAUDE.md

## Version ordering rule

In both `index.html` (the roadmap section, "Where it's headed") and `changelog.html` (the releases list), versions must always be ordered **newest shipped first, oldest shipped last, with any upcoming/unreleased entries at the very bottom**.

When adding a new shipped release, insert its block at the top of the shipped entries — above all previously shipped versions — and leave any "Upcoming" or "Next" entries after all shipped entries.

Example correct order: 2.1.10 → 2.1 → 2.0 → 1.3 → 1.2 → 1.0 → Android (Upcoming)

## Static-site build and publication

- Public pages are authored as HTML plus structured landing content under `content/landing/` and rendered with `python3 scripts/build_site.py` into `_site/`.
- Store URLs are maintained in `content/product.json`; do not add new hard-coded store destinations to page sources.
- Run `python3 scripts/check_site.py --dir _site` before browser tests.
- GitHub Pages must upload `_site/`, never the repository root. This keeps private evidence, docs, source content and tooling out of the public artifact.
- The production deploy workflow is restricted to `main`. Do not use `workflow_dispatch` from a feature branch to publish.
