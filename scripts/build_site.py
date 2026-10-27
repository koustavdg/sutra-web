#!/usr/bin/env python3
"""Build the explicitly public Sutra site files into _site/."""
from __future__ import annotations

import html
import json
import shutil
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "_site"
PUBLIC_FILES = [
    "index.html", "help.html", "changelog.html", "feedback.html",
    "privacy.html", "drm-free.html", "CNAME", "BingSiteAuth.xml",
]
PUBLIC_ASSETS = [
    "assets/app-icon.png", "assets/badge-appstore.svg", "assets/badge-googleplay.png",
    "assets/favicon.png", "assets/maple_leaf.png", "assets/sutra-preview-android.mp4",
    "assets/sutra-preview-ios.mp4", "assets/screenshots/01-library.png",
    "assets/screenshots/02-connect-landing.jpg", "assets/screenshots/05-comics.mp4",
    "assets/screenshots/05-comics-muted.mp4", "assets/screenshots/05-comics-poster.jpg",
    "assets/screenshots/06-autoscroll.mp4", "assets/screenshots/07-pro.png",
    "assets/screenshots/hero.png", "assets/screenshots/android/05-comics.mp4",
    "assets/screenshots/android/06-autoscroll.mp4", "assets/screenshots/android/07-pro.webp",
    "assets/screenshots/android/hero-library.webp", "assets/captions/panel-reading-en.vtt",
    "assets/demos/reading-demo-ios.mp4", "assets/demos/reading-demo-ios.jpg",
    "assets/demos/reading-demo-ios.vtt",
]
STORE_IOS = ""
STORE_ANDROID = ""
SITE_URL = "https://sutra-reader.com"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def li(items: list[str]) -> str:
    return "".join(f"<li>{esc(item)}</li>" for item in items)


def render_page(data: dict, template: str, all_pages: dict[str, dict]) -> str:
    slug = data["slug"]
    image = data["image"]
    media = (f'<video controls playsinline preload="metadata" poster="{esc(data["poster"])}" aria-label="{esc(data["image_alt"])}">'
             f'<source src="{esc(image)}" type="video/mp4"><track kind="captions" srclang="en" label="English captions" src="{esc(data["captions"])}" default></video>') if image.endswith(".mp4") else (
             f'<img src="{esc(image)}" alt="{esc(data["image_alt"])}" loading="lazy">')
    transcript = (f'<details><summary>Video transcript</summary><p>{esc(data["transcript"])}</p></details>'
                  if data.get("transcript") else "")
    rows = "".join("<tr>" + "".join(f"<td>{esc(cell)}</td>" for cell in row) + "</tr>"
                   for row in data["compatibility"])
    faq = "".join(f'<details><summary>{esc(item["q"])}</summary><p>{esc(item["a"])}</p></details>'
                  for item in data["faq"])
    related = "".join(f'<li><a href="{esc(name)}.html">{esc(all_pages[name]["link_name"])}</a></li>'
                      for name in data["related"])
    substitutions = {
        "title": esc(data["title"]), "description": esc(data["description"]),
        "canonical": esc(f"{SITE_URL}/{slug}.html"), "h1": esc(data["h1"]),
        "intro": esc(data["intro"]), "eyebrow": esc(data["eyebrow"]),
        "crumb": esc(data["link_name"]), "benefits": li(data["benefits"]),
        "compatibility": rows, "steps": li(data["steps"]),
        "limitations": li(data["limitations"]), "faq": faq,
        "help_url": esc(data["help_url"]), "proof_media": media,
        "image_alt": esc(data["image_alt"]), "related": related,
        "proof_intro": esc(data.get("proof_intro", "The screenshot shows Sutra's current library and connection flow. Follow the linked setup guide for details specific to your server and configuration.")),
        "transcript": transcript,
        "ios_store": STORE_IOS, "android_store": STORE_ANDROID,
    }
    for key, value in substitutions.items():
        template = template.replace("{{" + key + "}}", value)
    if "{{" in template:
        raise ValueError(f"Unresolved template token in {slug}")
    return template


def main() -> None:
    if OUT.exists():
        if OUT.resolve().parent != ROOT or OUT.name != "_site":
            raise RuntimeError(f"Refusing to clear unexpected output path: {OUT}")
        shutil.rmtree(OUT)
    OUT.mkdir()
    for relative in PUBLIC_FILES:
        shutil.copy2(ROOT / relative, OUT / relative)
    product = json.loads((ROOT / "content/product.json").read_text(encoding="utf-8"))
    stores = product["stores"]
    global STORE_IOS, STORE_ANDROID
    STORE_IOS = stores["ios"]["url"]
    STORE_ANDROID = stores["android"]["url"]
    for path in OUT.glob("*.html"):
        rendered = path.read_text(encoding="utf-8")
        rendered = rendered.replace("{{ios_store}}", esc(STORE_IOS))
        rendered = rendered.replace("{{android_store}}", esc(STORE_ANDROID))
        path.write_text(rendered, encoding="utf-8")
    for relative in PUBLIC_ASSETS:
        source = ROOT / relative
        if not source.is_file():
            raise FileNotFoundError(f"Public asset listed but missing: {relative}")
        destination = OUT / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    template = (ROOT / "templates/integration.html").read_text(encoding="utf-8")
    content_dir = ROOT / "content/landing"
    page_data = {}
    for path in sorted(content_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["slug"] != path.stem:
            raise ValueError(f"Landing slug must match filename: {path}")
        page_data[data["slug"]] = data
    if set(page_data) != {"kavita-reader", "komga-reader", "comic-panel-reader", "opds-reader", "calibre-reader"}:
        raise ValueError("Exactly the five planned integration pages must be present")
    for data in page_data.values():
        (OUT / f'{data["slug"]}.html').write_text(render_page(data, template, page_data), encoding="utf-8")

    agents = ["*", "Googlebot", "Bingbot", "OAI-SearchBot", "GPTBot", "Claude-SearchBot", "ClaudeBot", "PerplexityBot"]
    robots = "\n\n".join(f"User-agent: {agent}\nAllow: /" for agent in agents)
    (OUT / "robots.txt").write_text(robots + f"\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")

    urls = ["/", "/help.html", "/changelog.html", "/feedback.html", "/privacy.html", "/drm-free.html"]
    urls.extend(f"/{slug}.html" for slug in page_data)
    entries = "\n".join(f"  <url><loc>{SITE_URL}{path}</loc></url>" for path in urls)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n' + \
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + entries + \
        '\n</urlset>\n'
    (OUT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"Built {len(urls)} canonical pages to {OUT.relative_to(ROOT)} ({date.today().isoformat()}).")


if __name__ == "__main__":
    main()
