#!/usr/bin/env python3
"""Prove that a broken canonical is rejected without changing the built site."""
from pathlib import Path
import shutil
import tempfile

from check_site import check


def main() -> None:
    site = Path(__file__).resolve().parents[1] / "_site"
    with tempfile.TemporaryDirectory(prefix="sutra-quality-test-") as directory:
        fixture = Path(directory) / "site"
        shutil.copytree(site, fixture)
        page = fixture / "kavita-reader.html"
        content = page.read_text(encoding="utf-8")
        original = '<link rel="canonical" href="https://sutra-reader.com/kavita-reader.html">'
        if original not in content:
            raise SystemExit("Fixture setup failed: expected canonical not found")
        page.write_text(content.replace(original, "", 1), encoding="utf-8")
        try:
            check(fixture)
        except SystemExit as error:
            if "canonical should be exactly" not in str(error):
                raise SystemExit(f"Fixture failed for the wrong reason: {error}") from error
        else:
            raise SystemExit("Quality gate accepted a page without its canonical")
    print("Quality gate correctly rejected a missing canonical fixture.")


if __name__ == "__main__":
    main()
