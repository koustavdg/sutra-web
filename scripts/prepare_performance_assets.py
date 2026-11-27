#!/usr/bin/env python3
"""Generate responsive WebP derivatives and vendor the site's existing OFL fonts.

Original images are never modified. Requires macOS sips and cwebp. Font fetching
is an explicit maintenance command, never part of deployment or page loading.
"""
import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
from pathlib import Path
from site_enhancements import image_size

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'app-icon': ('assets/app-icon.png', [48, 96, 192]),
    'ios-hero': ('assets/optimized/ios-hero.webp', [240, 480, 600]),
    'ios-library': ('assets/optimized/ios-library.webp', [200, 400, 600]),
    'ios-pro': ('assets/optimized/ios-pro.webp', [200, 400, 600]),
    'android-library': ('assets/screenshots/android/hero-library.webp', [200, 400, 600]),
    'android-pro': ('assets/screenshots/android/07-pro.webp', [200, 400, 600]),
    'duo': ('assets/optimized/iphone-duo.webp', [480, 800, 1100]),
    'ios-poster': ('assets/sutra-preview-ios-poster.jpg', [240, 480]),
    'android-poster': ('assets/sutra-preview-android-poster.jpg', [240, 480]),
    'comics-poster': ('assets/screenshots/05-comics-poster.jpg', [240, 480]),
    'ios-scroll': ('assets/optimized/ios-autoscroll.jpg', [240, 480]),
    'android-scroll': ('assets/optimized/android-autoscroll.jpg', [240, 480]),
    'android-comics': ('assets/optimized/android-comics.jpg', [240, 480]),
}


def images():
    out = ROOT / 'assets/responsive'
    out.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, (source, widths) in SOURCES.items():
        variants = []
        original_width = image_size(ROOT / source)[0]
        with tempfile.TemporaryDirectory(prefix='sutra-image-') as temporary:
            png = Path(temporary) / 'source.png'
            subprocess.run(['sips', '-s', 'format', 'png', str(ROOT / source), '--out', str(png)],
                           check=True, capture_output=True)
            for width in widths:
                target = out / f'{name}-{width}.webp'
                # Never enlarge a small poster. Keep requested-size filenames
                # stable, but describe actual pixels in the responsive manifest.
                actual_width = min(width, original_width)
                quality = '78' if source.endswith('.jpg') else '84'
                subprocess.run(['cwebp', '-quiet', '-q', quality, '-m', '6', '-resize', str(actual_width), '0',
                                str(png), '-o', str(target)], check=True)
                variants.append({'width': actual_width, 'path': target.relative_to(ROOT).as_posix()})
        manifest[source] = variants
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(f'Generated {sum(map(len, manifest.values()))} responsive images; originals preserved.')


def download(url):
    request = urllib.request.Request(url, headers={'User-Agent':
        'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36'})
    return urllib.request.urlopen(request, timeout=30).read()


def fonts():
    out = ROOT / 'assets/fonts'
    out.mkdir(parents=True, exist_ok=True)
    url = ('https://fonts.googleapis.com/css2?family=Inter:wght@400..700'
           '&family=JetBrains+Mono:wght@400..500'
           '&family=Spectral:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap')
    css = download(url).decode()
    blocks = re.findall(r'/\* latin \*/\s*(@font-face\s*\{[^}]+\})', css)
    if len(blocks) != 8:
        raise ValueError(f'Expected 8 Latin font faces; got {len(blocks)}. Review upstream CSS.')
    local = []
    for block in blocks:
        remote = re.search(r'url\((https://[^)]+)\)', block)[1]
        filename = hashlib.sha256(remote.encode()).hexdigest()[:16] + '.woff2'
        (out / filename).write_bytes(download(remote))
        local.append(block.replace(remote, '/assets/fonts/' + filename))
    (out / 'fonts.css').write_text('\n'.join(local) + '\n')
    for family in ['inter', 'spectral', 'jetbrainsmono']:
        (out / f'{family}-OFL.txt').write_bytes(download(f'https://raw.githubusercontent.com/google/fonts/main/ofl/{family}/OFL.txt'))
    (out / 'sources.json').write_text(json.dumps({'css_source': url, 'subset': 'latin',
        'license': 'SIL Open Font License 1.1; see bundled *-OFL.txt files',
        'note': 'Existing font families and weights; other scripts use system fallbacks.'}, indent=2) + '\n')
    print('Vendored Inter, Spectral and JetBrains Mono with license files.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fonts', action='store_true', help='Also download licensed Latin WOFF2 fonts')
    args = parser.parse_args()
    images()
    if args.fonts:
        fonts()
