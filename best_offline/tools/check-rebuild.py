"""Regression check: a reused MkDocs config must not retain stale search content."""
import json
from pathlib import Path
import tempfile
from mkdocs.config import load_config
from mkdocs.commands.build import build

with tempfile.TemporaryDirectory(prefix="best-offline-rebuild-") as temporary:
    root = Path(temporary)
    docs = root / "docs"
    docs.mkdir()
    page = docs / "index.md"
    page.write_text("# Sample\n\nuniquelybefore\n", encoding="utf-8")
    config_file = root / "mkdocs.yml"
    config_file.write_text(
        "site_name: Rebuild check\nuse_directory_urls: false\n"
        "theme:\n  name: best_offline\nplugins:\n  - best-offline\n",
        encoding="utf-8")
    config = load_config(config_file=str(config_file), strict=True)
    build(config)
    data = root / "site" / "js" / "search-data.js"
    assert "uniquelybefore" in data.read_text(encoding="utf-8")
    page.write_text("# Sample\n\nuniquelyafter\n", encoding="utf-8")
    build(config)
    content = data.read_text(encoding="utf-8")
    assert "uniquelybefore" not in content, "Search retained content from the previous build"
    assert "uniquelyafter" in content
    entries = json.loads(content.split("window.BEST_OFFLINE_SEARCH = ", 1)[1].strip().rstrip(";"))
    assert len(entries) == 1, "Rebuild duplicated search entries"
print("PASS: reused config replaces search data after edits")
