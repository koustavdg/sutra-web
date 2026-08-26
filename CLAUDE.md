# Sutra Web — CLAUDE.md

## Version ordering rule

In both `index.html` (the roadmap section, "Where it's headed") and `changelog.html` (the releases list), versions must always be ordered **newest shipped first, oldest shipped last, with any upcoming/unreleased entries at the very bottom**.

When adding a new shipped release, insert its block at the top of the shipped entries — above all previously shipped versions — and leave any "Upcoming" or "Next" entries after all shipped entries.

Example correct order: 2.1.10 → 2.1 → 2.0 → 1.3 → 1.2 → 1.0 → Android (Upcoming)
