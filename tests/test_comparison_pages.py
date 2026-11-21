import json
import tempfile
import unittest
from pathlib import Path

from scripts.check_site import Page
from scripts.comparison_pages import BASE, HEADINGS, render_comparisons


class ComparisonPublicationTests(unittest.TestCase):
    def render(self, preview=False):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        out = Path(temp.name)
        render_comparisons(out, preview=preview)
        return out

    def test_public_pages_have_consistent_discovery_metadata(self):
        out = self.render()
        for slug in HEADINGS:
            with self.subTest(slug=slug):
                parser = Page()
                source = (out / f'{slug}.html').read_text()
                parser.feed(source)
                self.assertFalse(parser.noindex)
                url = f'{BASE}/{slug}.html'
                self.assertEqual(parser.canonical, [url])
                graph = json.loads(parser.jsonld[0])['@graph']
                page = next(n for n in graph if n['@type'] == 'WebPage')
                breadcrumbs = next(n for n in graph if n['@type'] == 'BreadcrumbList')
                self.assertEqual(page['url'], url)
                self.assertEqual(breadcrumbs['itemListElement'][-1]['item'], url)
                self.assertEqual(page['name'], ' '.join(parser.title_text))
                self.assertEqual(page['description'], parser.description_text[0])
                self.assertNotIn('/_site/', source)
                self.assertNotIn('{{', source)
                for link in page['citation']:
                    self.assertIn(link, source)
                self.assertFalse(any(n['@type'] in ('Review', 'AggregateRating') for n in graph))

    def test_editorial_previews_cannot_claim_canonical_publication(self):
        out = self.render(preview=True)
        for slug in HEADINGS:
            parser = Page()
            parser.feed((out / f'{slug}.html').read_text())
            self.assertTrue(parser.noindex)
            self.assertEqual(parser.canonical, [])
            self.assertEqual(parser.jsonld, [])

    def test_all_pages_explain_streaming_requirements_and_offline_downloads(self):
        out = self.render()
        for slug in HEADINGS:
            with self.subTest(slug=slug):
                source = (out / f'{slug}.html').read_text()
                self.assertIn('Start large comics without the full download', source)
                self.assertIn('With Sutra Pro', source)
                self.assertIn('supported Kavita and Komga servers', source)
                self.assertIn('without downloading the whole archive first', source)
                self.assertIn('Individual pages still transfer and may be cached', source)
                self.assertIn('download the complete book for offline reading', source)
                self.assertIn('Komga requires Page Streaming permission', source)

    def test_hub_item_list_has_contiguous_positions_and_rendered_links(self):
        out = self.render()
        source = (out / 'compare-readers.html').read_text()
        parser = Page()
        parser.feed(source)
        graph = json.loads(parser.jsonld[0])['@graph']
        items = next(n for n in graph if n['@type'] == 'ItemList')['itemListElement']
        self.assertEqual([item['position'] for item in items], [1, 2])
        for item in items:
            self.assertIn(item['url'].removeprefix(BASE + '/'), source)


if __name__ == '__main__':
    unittest.main()
