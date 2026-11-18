"""Small end-to-end fixtures for authoring errors in generated HTML."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("site_audit", str(Path(__file__).with_name("check-site.py")))
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)


class AnchorAudit(unittest.TestCase):
    def check_html(self, html):
        with tempfile.TemporaryDirectory(prefix="best-offline-audit-") as temporary:
            site = Path(temporary)
            (site / "index.html").write_text(html, encoding="utf-8")
            (site / "js").mkdir()
            (site / "js" / "search-data.js").write_text(
                'window.BEST_OFFLINE_SEARCH = [{"url":"index.html#details"}];', encoding="utf-8")
            with contextlib.redirect_stdout(io.StringIO()):
                audit.check(site)

    def test_linked_declaration_and_target(self):
        self.check_html('<pre><code><a href="#details">ReadSamples</a>()</code></pre><h2 id="details">Details</h2>')

    def test_duplicate_detail_ids_are_rejected(self):
        with self.assertRaisesRegex(SystemExit, "duplicate anchor id details"):
            self.check_html('<h2 id="details">First</h2><h2 id="details">Second</h2>')

    def test_missing_same_page_destination_is_rejected(self):
        with self.assertRaisesRegex(SystemExit, "missing anchor #missing"):
            self.check_html('<a href="#missing">ReadSamples</a><h2 id="details">Details</h2>')


if __name__ == "__main__":
    unittest.main()
