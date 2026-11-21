"""Deterministic publication enhancements; no network or browser dependencies."""
import html
import json
import re
import struct
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOCIAL_IMAGE = 'https://sutra-reader.com/assets/social-card.png'


def entitlement_rows():
    product = json.loads((ROOT / 'content/product.json').read_text())
    rows = []
    for row in product['home_entitlements']:
        if 'group' in row:
            rows.append('<tr class="group"><td colspan="3">' + html.escape(row['group']) + '</td></tr>')
            continue
        label = html.escape(row['label'])
        if row['note']:
            label += '<small>' + html.escape(row['note']) + '</small>'
        cells = ''.join('<td><span class="' + ('n' if value == 'Pro required' else 'y') + '">'
                        + html.escape(value) + '</span></td>' for value in [row['free'], row['pro']])
        rows.append('<tr><th scope="row">' + label + '</th>' + cells + '</tr>')
    return '\n'.join(rows)


def inline(text):
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: f'<a href="{m[2]}">{m[1]}</a>', text)
    return re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)


def policy_html(markdown):
    """Render the deliberately small Markdown subset used by the approved policies."""
    blocks = []
    for block in re.split(r'\n\s*\n', markdown.strip()):
        if block.startswith('# '):
            continue  # Page and platform labels provide the document heading.
        if block.startswith('## '):
            blocks.append('<h3>' + inline(block[3:]) + '</h3>')
        elif block.startswith('- '):
            items = re.split(r'\n(?=- )', block)
            blocks.append('<ul>' + ''.join('<li>' + inline(' '.join(x[2:].splitlines())) + '</li>' for x in items) + '</ul>')
        else:
            blocks.append('<p>' + inline(' '.join(block.splitlines())) + '</p>')
    return '\n'.join(blocks)


def privacy_panels():
    result = []
    for platform, name in [('ios', 'PRIVACY.md'), ('android', 'PRIVACY-ANDROID.md')]:
        markdown = (ROOT / 'content/policies' / name).read_text()
        markdown = markdown.replace('](PRIVACY.md)', '](#ios)')
        result.append(f'<section id="{platform}" class="policy-panel" aria-labelledby="policy-{platform}-title">'
                      f'<h2 id="policy-{platform}-title">{"iOS" if platform == "ios" else "Android"} privacy policy</h2>'
                      + policy_html(markdown) + '</section>')
    return '\n'.join(result)


def image_size(path):
    data = path.read_bytes()
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        return struct.unpack('>II', data[16:24])
    if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        kind = data[12:16]
        if kind == b'VP8X':
            return (1 + int.from_bytes(data[24:27], 'little'),
                    1 + int.from_bytes(data[27:30], 'little'))
        if kind == b'VP8 ':
            width, height = struct.unpack('<HH', data[26:30])
            return width & 0x3fff, height & 0x3fff
        if kind == b'VP8L':
            packed = int.from_bytes(data[21:25], 'little')
            return (packed & 0x3fff) + 1, ((packed >> 14) & 0x3fff) + 1
    if data.startswith(b'\xff\xd8'):
        pos = 2
        while pos + 4 < len(data):
            if data[pos] != 0xff:
                pos += 1
                continue
            marker = data[pos + 1]
            if marker == 0xff:
                pos += 1
                continue
            if marker in {0xd8, 0xd9}:
                pos += 2
                continue
            length = int.from_bytes(data[pos + 2:pos + 4], 'big')
            if marker in {0xc0, 0xc1, 0xc2, 0xc3}:
                height, width = struct.unpack('>HH', data[pos + 5:pos + 9])
                return width, height
            pos += 2 + max(length, 2)
    return None


class Images(HTMLParser):
    def __init__(self):
        super().__init__()
        self.replacements = []

    def handle_starttag(self, tag, attrs):
        if tag != 'img':
            return
        a = dict(attrs)
        raw = self.get_starttag_text()
        # Existing explicit dimensions describe the intended aspect ratio.
        if 'width' in a and 'height' in a:
            return
        src = a.get('src', '').split('?')[0].lstrip('/')
        path = ROOT / src
        size = image_size(path) if path.is_file() else None
        if src == 'assets/badge-appstore.svg':
            size = (120, 40)
        if size:
            width, height = size
            updated = re.sub(r'\s+(?:width|height)="[^"]*"', '', raw)
            self.replacements.append((raw, updated[:-1] + f' width="{width}" height="{height}">'))


def enhance_page(source):
    source = re.sub(r'href="(?:https://sutra-reader\.com/|/)?index\.html(#[^"]*)?"',
                    lambda m: 'href="/' + (m[1] or '') + '"', source)
    if '<main' not in source:
        source = source.replace('</header>', '</header>\n<main id="main-content">', 1)
        source = source.replace('<footer', '</main>\n<footer', 1)
    source = source.replace('property="og:image" content="https://sutra-reader.com/assets/app-icon.png"',
                            f'property="og:image" content="{SOCIAL_IMAGE}"')
    source = source.replace('property="og:image:alt" content="Sutra app icon"',
                            'property="og:image:alt" content="Sutra — DRM-free ebook and comic reader for iOS and Android"')
    if 'property="og:image"' not in source:
        source = source.replace('</head>', f'<meta property="og:image" content="{SOCIAL_IMAGE}">\n'
                               '<meta property="og:image:width" content="1200">\n'
                               '<meta property="og:image:height" content="630">\n'
                               '<meta property="og:image:alt" content="Sutra — DRM-free ebook and comic reader for iOS and Android">\n</head>')
    # Also make the image explicit to clients that don't fall back to Open Graph.
    if 'name="twitter:image"' not in source:
        match = re.search(r'property="og:image" content="([^"]+)"', source)
        source = source.replace('</head>', f'<meta name="twitter:image" content="{match[1]}">\n</head>')
    source = source.replace('name="twitter:card" content="summary"',
                            'name="twitter:card" content="summary_large_image"')
    if 'property="og:image:width"' not in source:
        source = source.replace('</head>', '<meta property="og:image:width" content="1200">\n'
                               '<meta property="og:image:height" content="630">\n</head>')
    source = source.replace('color:#9880BB;', 'color:#C9B8E8;')
    images = Images()
    images.feed(source)
    for old, new in images.replacements:
        source = source.replace(old, new)
    return source
