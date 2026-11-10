#!/usr/bin/env python3
"""Notify IndexNow of changes since the last fully successful deployment."""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

HOST = "sutra-reader.com"
KEY = "7967774caec5b198d5114f406735e218"
KEY_URL = f"https://{HOST}/{KEY}.txt"
ENDPOINT = "https://api.indexnow.org/indexnow"
SITEMAP = Path(__file__).resolve().parents[1] / "_site" / "sitemap.xml"
ROOT = SITEMAP.parent.parent


def sitemap_urls(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    urls = [node.text.strip() for node in root.findall("{*}url/{*}loc") if node.text]
    if not urls or len(urls) != len(set(urls)):
        raise ValueError("Sitemap must contain unique canonical URLs")
    for url in urls:
        parsed = urllib.parse.urlsplit(url)
        if parsed.scheme != "https" or parsed.netloc != HOST or parsed.query or parsed.fragment:
            raise ValueError(f"Unexpected sitemap URL: {url}")
    return urls


def page_path(site: Path, url: str) -> Path:
    path = urllib.parse.urlsplit(url).path
    return site / ("index.html" if path == "/" else path.lstrip("/"))


def changed_urls(previous: Path, current: Path) -> list[str]:
    old_urls = set(sitemap_urls(previous / "sitemap.xml"))
    new_urls = set(sitemap_urls(current / "sitemap.xml"))
    changed = old_urls ^ new_urls
    old_assets = previous / "assets"
    new_assets = current / "assets"
    assets = {p.relative_to(old_assets) for p in old_assets.rglob("*") if p.is_file()}
    assets |= {p.relative_to(new_assets) for p in new_assets.rglob("*") if p.is_file()}
    changed_assets = []
    for asset in assets:
        before, after = old_assets / asset, new_assets / asset
        if not before.is_file() or not after.is_file() or before.read_bytes() != after.read_bytes():
            changed_assets.append("assets/" + asset.as_posix())
    for url in old_urls & new_urls:
        before = page_path(previous, url).read_bytes()
        after = page_path(current, url).read_bytes()
        if before != after or any(asset.encode() in before or asset.encode() in after for asset in changed_assets):
            changed.add(url)
    return sorted(changed)


def previous_successful_sha() -> str:
    repository = os.environ["GITHUB_REPOSITORY"]
    token = os.environ["GH_TOKEN"]
    endpoint = f"https://api.github.com/repos/{repository}/actions/workflows/deploy-pages.yml/runs?branch=main&status=success&per_page=100"
    request = urllib.request.Request(endpoint, headers={"Authorization": f"Bearer {token}", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        runs = json.load(response)["workflow_runs"]
    for run in runs:
        sha = run["head_sha"]
        if subprocess.run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], cwd=ROOT, check=False).returncode == 0:
            return sha
    raise RuntimeError("No previous successful deployment found; cannot safely determine changed or deleted pages")


def build_previous(sha: str, directory: Path) -> Path:
    archive = directory / "previous.tar"
    with archive.open("wb") as output:
        subprocess.run(["git", "archive", "--format=tar", sha], cwd=ROOT, stdout=output, check=True)
    with tarfile.open(archive) as source:
        source.extractall(directory / "source", filter="data")
    source_dir = directory / "source"
    subprocess.run([sys.executable, "scripts/build_site.py"], cwd=source_dir, check=True)
    return source_dir / "_site"


def wait_for_live_key() -> None:
    for attempt in range(12):
        try:
            request = urllib.request.Request(KEY_URL, headers={"Cache-Control": "no-cache"})
            with urllib.request.urlopen(request, timeout=15) as response:
                if response.read().decode("utf-8").strip() == KEY:
                    return
        except (urllib.error.URLError, TimeoutError, UnicodeDecodeError) as exc:
            print(f"Waiting for the IndexNow key to become public: {exc}", flush=True)
        if attempt < 11:
            time.sleep(10)
    raise RuntimeError("The public IndexNow verification key did not become available")


def main() -> None:
    sha = previous_successful_sha()
    print(f"Comparing with the last successful deployment: {sha}", flush=True)
    with tempfile.TemporaryDirectory(prefix="sutra-indexnow-") as temporary:
        previous = build_previous(sha, Path(temporary))
        urls = changed_urls(previous, SITEMAP.parent)
    if not urls:
        print("No canonical pages changed; skipping IndexNow.")
        return
    wait_for_live_key()
    payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_URL, "urlList": urls}).encode()
    request = urllib.request.Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f"IndexNow accepted {len(urls)} canonical URLs (HTTP {response.status}).")


if __name__ == "__main__":
    main()
