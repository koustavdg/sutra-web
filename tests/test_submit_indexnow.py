import tempfile
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from scripts.submit_indexnow import changed_urls, previous_successful_sha, sitemap_urls


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


class IndexNowChangeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.old = Path(self.temp.name) / "old"
        self.new = Path(self.temp.name) / "new"
        for site in (self.old, self.new):
            site.mkdir()
            (site / "assets").mkdir()

    def site(self, directory, pages, assets=None):
        entries = []
        for path, contents in pages.items():
            (directory / ("index.html" if path == "/" else path.lstrip("/"))).write_text(contents)
            entries.append(f"<url><loc>https://sutra-reader.com{path}</loc></url>")
        (directory / "sitemap.xml").write_text('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(entries) + "</urlset>")
        for name, contents in (assets or {}).items():
            (directory / "assets" / name).write_text(contents)

    def test_unchanged_site_skips_submission(self):
        for site in (self.old, self.new):
            self.site(site, {"/": "home", "/help.html": "help"})
        self.assertEqual(changed_urls(self.old, self.new), [])

    def test_changed_added_and_deleted_pages(self):
        self.site(self.old, {"/": "before", "/old.html": "old", "/same.html": "same"})
        self.site(self.new, {"/": "after", "/new.html": "new", "/same.html": "same"})
        self.assertEqual(changed_urls(self.old, self.new), ["https://sutra-reader.com/", "https://sutra-reader.com/new.html", "https://sutra-reader.com/old.html"])

    def test_shared_assets_notify_referencing_pages_only(self):
        pages = {"/": '<img src="assets/shared.png">', "/help.html": '<img src="assets/shared.png">', "/about.html": "unrelated"}
        self.site(self.old, pages, {"shared.png": "old"})
        self.site(self.new, pages, {"shared.png": "new"})
        self.assertEqual(changed_urls(self.old, self.new), ["https://sutra-reader.com/", "https://sutra-reader.com/help.html"])


class IndexNowBaselineTests(unittest.TestCase):
    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "test"})
    @patch("scripts.submit_indexnow.subprocess.run")
    @patch("scripts.submit_indexnow.urllib.request.urlopen")
    def test_selects_latest_successful_ancestor(self, urlopen, run):
        urlopen.return_value.__enter__.return_value = BytesIO(b'{"workflow_runs":[{"head_sha":"unrelated"},{"head_sha":"previous"}]}')
        run.side_effect = [unittest.mock.Mock(returncode=1), unittest.mock.Mock(returncode=0)]
        self.assertEqual(previous_successful_sha(), "previous")

    @patch.dict("os.environ", {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "test"})
    @patch("scripts.submit_indexnow.urllib.request.urlopen")
    def test_missing_baseline_fails_instead_of_silently_missing_deletions(self, urlopen):
        urlopen.return_value.__enter__.return_value = BytesIO(b'{"workflow_runs":[]}')
        with self.assertRaisesRegex(RuntimeError, "No previous successful deployment"):
            previous_successful_sha()


if __name__ == "__main__":
    unittest.main()
