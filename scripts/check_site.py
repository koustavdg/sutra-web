#!/usr/bin/env python3
"""Deterministic quality checks for the public static site artifact."""
from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://sutra-reader.com"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = 0
        self.title_text = []
        self.description = 0
        self.description_text = []
        self.canonical = []
        self.h1 = 0
        self.ids = set()
        self.links = []
        self.jsonld = []
        self.noindex = False
        self._in_title = False
        self._in_json = False
        self._json_buf = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                raise ValueError(f"duplicate id #{a['id']}")
            self.ids.add(a["id"])
        if tag == "title":
            self.title += 1
            self._in_title = True
        elif tag == "meta" and a.get("name", "").lower() == "description":
            if a.get("content", "").strip():
                self.description += 1
                self.description_text.append(a["content"].strip())
        elif tag == "meta" and a.get("name", "").lower() in {"robots", "googlebot"}:
            self.noindex = self.noindex or "noindex" in a.get("content", "").lower()
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical.append(a.get("href", ""))
        elif tag == "h1":
            self.h1 += 1
        elif tag == "script" and a.get("type") == "application/ld+json":
            self._in_json = True
            self._json_buf = []
        if tag in ("a", "img", "video", "source", "track"):
            for key in ("href", "src"):
                if a.get(key):
                    self.links.append((tag, key, a[key], a.get("alt")))

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag == "script" and self._in_json:
            self._in_json = False
            self.jsonld.append("".join(self._json_buf))

    def handle_data(self, data):
        if self._in_title and data.strip():
            self.title_text.append(data.strip())
        if self._in_json:
            self._json_buf.append(data)


def canonical_path(value: str) -> str:
    path = urlparse(value).path
    return path or "/"


def check(site: Path) -> None:
    pages = sorted(site.glob("*.html"))
    if not pages:
        raise SystemExit("No HTML pages found in site artifact")
    parsed = {}
    errors = []
    titles = {}
    descriptions = {}
    for path in pages:
        parser = Page()
        try:
            parser.feed(path.read_text(encoding="utf-8"))
        except Exception as e:
            errors.append(f"{path.name}: HTML parse error: {e}")
            continue
        parsed[path.name] = parser
        if any(token in path.read_text(encoding="utf-8") for token in ("{{ios_store}}", "{{android_store}}", "{{pro_price_usd}}")):
            errors.append(f"{path.name}: unresolved store or price token")
        if parser.title != 1:
            errors.append(f"{path.name}: expected one title")
        if not parser.title_text:
            errors.append(f"{path.name}: title must not be empty")
        else:
            title_text = " ".join(parser.title_text)
            if title_text in titles:
                errors.append(f"{path.name}: title duplicates {titles[title_text]}")
            titles[title_text] = path.name
        if parser.description != 1:
            errors.append(f"{path.name}: expected one non-empty meta description")
        elif parser.description_text[0] in descriptions:
            errors.append(f"{path.name}: meta description duplicates {descriptions[parser.description_text[0]]}")
        else:
            descriptions[parser.description_text[0]] = path.name
        if parser.h1 != 1:
            errors.append(f"{path.name}: expected exactly one H1, found {parser.h1}")
        if parser.noindex:
            errors.append(f"{path.name}: unintended noindex directive")
        expected = BASE + ("/" if path.name == "index.html" else "/" + path.name)
        if parser.canonical != [expected]:
            errors.append(f"{path.name}: canonical should be exactly {expected}; got {parser.canonical}")
        for raw in parser.jsonld:
            try:
                data = json.loads(raw)
                if isinstance(data, dict) and ("aggregateRating" in data or "review" in data):
                    errors.append(f"{path.name}: app rating/review schema needs verified evidence")
            except json.JSONDecodeError as e:
                errors.append(f"{path.name}: invalid JSON-LD: {e}")

    try:
        product = json.loads((ROOT / "content/product.json").read_text(encoding="utf-8"))
        claims = {item["id"]: item for item in product["capabilities"]}
        price_entries = [item for item in product["pricing"]["numeric_offers"]
                         if item.get("tier") == "pro" and item.get("currency") == "USD"]
        if len(price_entries) != 1 or not all(price_entries[0].get(key) for key in ("verified_at", "verified_by", "review_owner")):
            errors.append("USD Pro price must have an owner, verifier and verification date")
        elif "index.html" in parsed:
            expected_price = price_entries[0]["amount"]
            home_source = (site / "index.html").read_text(encoding="utf-8")
            app_nodes = [json.loads(raw) for raw in parsed["index.html"].jsonld
                         if json.loads(raw).get("@type") == "SoftwareApplication"]
            offers = app_nodes[0].get("offers", []) if len(app_nodes) == 1 else []
            if not any(offer.get("name") == "Sutra Pro in-app purchase" and offer.get("price") == expected_price and offer.get("priceCurrency") == "USD" for offer in offers):
                errors.append("Homepage schema must match the owner-verified USD Pro price")
            if f"${expected_price} USD" not in home_source:
                errors.append("Homepage must display the verified USD Pro price")
        for content_path in (ROOT / "content/landing").glob("*.json"):
            data = json.loads(content_path.read_text(encoding="utf-8"))
            if not data.get("claim_ids"):
                errors.append(f"{content_path.name}: no capability-matrix claim IDs declared")
            for claim_id in data.get("claim_ids", []):
                if claim_id not in claims:
                    errors.append(f"{content_path.name}: unknown capability claim ID {claim_id}")
                elif claims[claim_id].get("status") not in {"verified", "unsupported"} or not claims[claim_id].get("approved_at"):
                    errors.append(f"{content_path.name}: capability claim {claim_id} lacks owner approval")
            copy = json.dumps(data, ensure_ascii=False).lower()
            if re.search(r"\$\s*\d|\bbest\b|same features on ios and android|all servers stream", copy):
                errors.append(f"{content_path.name}: contains a prohibited evergreen claim/price")
    except (OSError, json.JSONDecodeError, KeyError) as e:
        errors.append(f"Capability/content validation failed: {e}")

    for name, parser in parsed.items():
        source = site / name
        for tag, key, raw, alt in parser.links:
            if tag == "img" and alt is None:
                errors.append(f"{name}: image missing alt text: {raw}")
            u = urlparse(raw)
            if u.scheme or raw.startswith("//"):
                continue
            target = (site / u.path) if u.path else source
            if u.path.startswith("/"):
                target = site / u.path.lstrip("/")
            if u.path and not target.exists():
                errors.append(f"{name}: missing local {key}: {raw}")
            elif u.fragment and target.suffix == ".html" and target.exists():
                target_parser = parsed.get(target.name)
                if target_parser and u.fragment not in target_parser.ids:
                    errors.append(f"{name}: missing fragment target: {raw}")
        source_html = source.read_text(encoding="utf-8")
        if name.endswith("-reader.html") and "<video" in source_html and ('kind="captions"' not in source_html or "Video transcript" not in source_html):
            errors.append(f"{name}: video requires captions and a visible transcript")

    sitemap = site / "sitemap.xml"
    try:
        root = ET.parse(sitemap).getroot()
        locs = [el.text for el in root.iter() if el.tag.endswith("loc")]
        if len(locs) != len(set(locs)):
            errors.append("sitemap.xml: duplicate canonical URL")
        expected_urls = {BASE + ("/" if page.name == "index.html" else "/" + page.name) for page in pages}
        if set(locs) != expected_urls:
            errors.append("sitemap.xml: canonical URLs do not match the public HTML pages")
        for loc in locs:
            path = canonical_path(loc)
            target = site / ("index.html" if path == "/" else path.lstrip("/"))
            if not target.exists():
                errors.append(f"sitemap.xml: URL has no local page: {loc}")
        for slug in ("kavita-reader", "komga-reader", "comic-panel-reader", "opds-reader", "calibre-reader"):
            if f"{BASE}/{slug}.html" not in locs:
                errors.append(f"sitemap.xml: missing {slug}.html")
    except (OSError, ET.ParseError) as e:
        errors.append(f"sitemap.xml: invalid or missing: {e}")

    robots_path = site / "robots.txt"
    if not robots_path.exists():
        errors.append("robots.txt is missing")
    else:
        robots = robots_path.read_text(encoding="utf-8")
        for agent in ("Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "Claude-SearchBot", "ClaudeBot", "PerplexityBot"):
            if not re.search(rf"User-agent:\s*{re.escape(agent)}\s*\nAllow:\s*/", robots, re.I):
                errors.append(f"robots.txt: {agent} must be explicitly allowed")
        if "https://sutra-reader.com/sitemap.xml" not in robots:
            errors.append("robots.txt: sitemap declaration missing")

    prohibited = {"docs", "scripts", "templates", "content", ".git", ".github"}
    if prohibited.intersection(child.name for child in site.iterdir()):
        errors.append("public artifact contains internal source or tooling directories")
    if any(".env" in p.name or "evidence" in p.name.lower() for p in site.rglob("*")):
        errors.append("public artifact contains a private config/evidence-like path")
    for path in site.glob("*-reader.html"):
        if path.stat().st_size > 100_000:
            errors.append(f"{path.name}: generated HTML exceeds 100 KB")
    for relative in ("assets/screenshots/02-connect-landing.jpg", "assets/screenshots/05-comics-poster.jpg"):
        path = site / relative
        if path.exists() and path.stat().st_size > 300_000:
            errors.append(f"{relative}: new landing-page image exceeds 300 KB")
    video = site / "assets/screenshots/05-comics-muted.mp4"
    if video.exists() and video.stat().st_size > 5_000_000:
        errors.append("comic demonstration video exceeds 5 MB")
    if errors:
        raise SystemExit("Site checks failed:\n- " + "\n- ".join(errors))
    print(f"Site checks passed: {len(pages)} HTML pages, sitemap, robots, local links and metadata.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    check(args.dir.resolve())
