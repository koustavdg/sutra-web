import tempfile
import unittest
from pathlib import Path

from scripts.submit_indexnow import sitemap_urls


class IndexNowSitemapTests(unittest.TestCase):
    def parse(self, urls):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sitemap.xml"
            items = "".join(f"<url><loc>{url}</loc></url>" for url in urls)
            path.write_text(f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{items}</urlset>')
            return sitemap_urls(path)

    def test_accepts_canonical_sutra_urls(self):
        urls = ["https://sutra-reader.com/", "https://sutra-reader.com/iphone-duo.html"]
        self.assertEqual(self.parse(urls), urls)

    def test_rejects_other_hosts_and_duplicate_urls(self):
        for urls in (["https://example.com/"], ["https://sutra-reader.com/"] * 2, []):
            with self.subTest(urls=urls), self.assertRaises(ValueError):
                self.parse(urls)


if __name__ == "__main__":
    unittest.main()
