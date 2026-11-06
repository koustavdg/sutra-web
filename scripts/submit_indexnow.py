#!/usr/bin/env python3
"""Notify IndexNow about the canonical pages after a successful deployment."""
from __future__ import annotations

import json
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
    urls = sitemap_urls(SITEMAP)
    wait_for_live_key()
    payload = json.dumps({"host": HOST, "key": KEY, "keyLocation": KEY_URL, "urlList": urls}).encode()
    request = urllib.request.Request(ENDPOINT, data=payload, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
    with urllib.request.urlopen(request, timeout=30) as response:
        print(f"IndexNow accepted {len(urls)} canonical URLs (HTTP {response.status}).")


if __name__ == "__main__":
    main()
