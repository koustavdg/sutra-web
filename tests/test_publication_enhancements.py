import json
import hashlib
import re
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.product_facts import expand_facts, product_values
from scripts.site_enhancements import enhance_page, entitlement_rows, policy_html, privacy_panels, image_size, responsive_manifest

ROOT = Path(__file__).resolve().parents[1]


class PublicationEnhancementTests(unittest.TestCase):
    def test_policy_snapshots_match_recorded_source_hashes(self):
        sources = json.loads((ROOT / 'content/policies/sources.json').read_text())
        for name, source in sources.items():
            with self.subTest(name=name):
                self.assertEqual(hashlib.sha256((ROOT / 'content/policies' / name).read_bytes()).hexdigest(), source['sha256'])

    def test_policy_snapshots_render_both_platforms_without_script(self):
        panels = privacy_panels()
        self.assertIn('id="ios"', panels)
        self.assertIn('id="android"', panels)
        self.assertIn('iOS Keychain', panels)
        self.assertIn('Android Keystore', panels)
        self.assertIn('Effective June 2026', panels)
        self.assertIn('Effective October 2026', panels)
        self.assertNotIn('<script', panels)
        self.assertNotIn('<h1', panels)
        self.assertIn('href="#ios"', panels)

    def test_policy_render_preserves_words_and_escapes_html(self):
        text = '# Privacy Policy\n\nEffective June 2026\n\n## Storage\n\n- **Books** — local\n  and offline\n- <tag>\n\n[Contact](https://example.com)'
        rendered = policy_html(text)
        self.assertIn('<h3>Storage</h3>', rendered)
        self.assertIn('<li><strong>Books</strong> — local   and offline</li>', rendered)
        self.assertIn('&lt;tag&gt;', rendered)
        self.assertIn('href="https://example.com"', rendered)

    def test_shared_facts_resolve_and_unknown_facts_fail(self):
        self.assertEqual(expand_facts('${{product.pro_price_usd}}'), '$6.99')
        with self.assertRaises(ValueError):
            expand_facts('{{product.missing}}')
        with patch('scripts.product_facts.product_values', return_value={**product_values(), 'pro_price_usd': '8.99'}):
            self.assertEqual(expand_facts(entitlement_rows()).count('$8.99 USD'), 1)

    def test_entitlement_cells_have_real_text(self):
        rows = expand_facts(entitlement_rows())
        self.assertIn('Included', rows)
        self.assertIn('Pro required', rows)
        self.assertIn('$6.99 USD', rows)
        self.assertNotIn('<svg', rows)
        self.assertNotIn('See store', rows)

    def test_release_and_tablet_facts_are_shared_and_owner_confirmed(self):
        values = product_values()
        self.assertEqual(values['ios_release'], '2.5.0')
        self.assertEqual(values['android_release'], '1.3.0')
        for name in ['index.html', 'help.html', 'llms.txt', 'llms-full.txt']:
            text = expand_facts((ROOT / name).read_text())
            self.assertIn(values['tablet_layout'], text)
            self.assertIn(values['comic_spread_status'], text)

    def test_built_assets_are_responsive_and_fonts_are_local(self):
        for page in (ROOT / '_site').glob('*.html'):
            source = page.read_text()
            self.assertNotIn('fonts.googleapis.com', source, page.name)
            self.assertNotIn('fonts.gstatic.com', source, page.name)
            self.assertIn('srcset=', source, page.name)
        source = (ROOT / '_site/index.html').read_text()
        self.assertLess(source.index('id="lane-ios-post"'), source.index('id="lane-parity"'))

    def test_responsive_descriptors_match_pixels_and_derivatives_do_not_upscale(self):
        for original, variants in responsive_manifest().items():
            source = ROOT / original
            for variant in variants:
                width, height = image_size(ROOT / variant['path'])
                self.assertEqual(width, variant['width'], variant['path'])
                self.assertLessEqual(width, image_size(source)[0], variant['path'])
                self.assertGreater(height, 0)
            fallback = ROOT / variants[min(1, len(variants) - 1)]['path']
            self.assertLess(fallback.stat().st_size, source.stat().st_size, original)

    def test_metadata_main_and_home_normalization_are_idempotent(self):
        source = '<html><head></head><body><header></header><a href="index.html#compare">Home</a><footer></footer></body></html>'
        enhanced = enhance_page(source)
        self.assertEqual(enhanced, enhance_page(enhanced))
        self.assertIn('href="/#compare"', enhanced)
        self.assertEqual(enhanced.count('<main'), 1)
        self.assertEqual(enhanced.count('property="og:image"'), 1)
        self.assertEqual(enhanced.count('name="twitter:image"'), 1)

    def test_built_pages_have_discovery_metadata_and_no_tokens(self):
        for page in (ROOT / '_site').glob('*.html'):
            source = page.read_text()
            with self.subTest(page=page.name):
                self.assertEqual(source.count('<main'), 1)
                self.assertIn('property="og:image"', source)
                self.assertIn('name="twitter:image"', source)
                self.assertNotRegex(source, r'href="(?:/)?index\.html')
                self.assertNotIn('{{', source)


if __name__ == '__main__':
    unittest.main()
