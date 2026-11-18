"""Check generated pages and active stylesheets without network access."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.resources = []
        self.links = []
        self.styles = []
        self.ids = set()
        self.duplicate_ids = set()
        self.in_style = False

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get("id"):
            if attrs["id"] in self.ids:
                self.duplicate_ids.add(attrs["id"])
            self.ids.add(attrs["id"])
        for key in ("src", "poster", "data"):
            if attrs.get(key) and (key != "data" or tag == "object"):
                self.resources.append(attrs[key])
        if attrs.get("srcset") and not attrs["srcset"].startswith("data:"):
            self.resources.extend(part.strip().split()[0] for part in attrs["srcset"].split(",") if part.strip())
        if tag == "link" and attrs.get("href"):
            self.resources.append(attrs["href"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if attrs.get("style"):
            self.styles.append(attrs["style"])
        if tag == "style":
            self.in_style = True

    def handle_endtag(self, tag):
        if tag == "style":
            self.in_style = False

    def handle_data(self, data):
        if self.in_style:
            self.styles.append(data)


def check(site):
    site = Path(site).resolve()
    errors, checked_css, pages = [], set(), {}
    for path in sorted(site.rglob("*.html")):
        parser = Page()
        parser.feed(path.read_text(encoding="utf-8"))
        pages[path] = parser

    def resource(origin, value, required=True):
        parsed = urlsplit(value)
        if value.startswith("//") or parsed.scheme in ("http", "https"):
            if required:
                errors.append("{}: remote resource {}".format(origin.relative_to(site), value))
            return
        if parsed.scheme in ("data", "mailto", "tel"):
            return
        if parsed.scheme or parsed.path.startswith("/"):
            errors.append("{}: nonportable URL {}".format(origin.relative_to(site), value))
            return
        if not parsed.path:
            if not required and parsed.fragment and origin in pages and unquote(parsed.fragment) not in pages[origin].ids:
                errors.append("{}: missing anchor {}".format(origin.relative_to(site), value))
            return
        target = (origin.parent / unquote(parsed.path)).resolve()
        try:
            target.relative_to(site)
        except ValueError:
            errors.append("{}: resource escapes site: {}".format(origin, value))
            return
        if not target.is_file():
            errors.append("{}: missing file {}".format(origin.relative_to(site), value))
        elif required and target.suffix.lower() == ".css" and target not in checked_css:
            checked_css.add(target)
            css(target, target.read_text(encoding="utf-8"))
        if not required and parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
            errors.append("{}: missing anchor {}".format(origin.relative_to(site), value))

    def css(origin, content):
        content = re.sub(r"/\*.*?\*/", "", content, flags=re.S)
        for match in re.finditer(r"url\(\s*['\"]?([^)'\"\s]+)", content):
            resource(origin, match.group(1))
        for match in re.finditer(r"@import\s+['\"]([^'\"]+)", content):
            resource(origin, match.group(1))

    for path, page in pages.items():
        for identifier in sorted(page.duplicate_ids):
            errors.append("{}: duplicate anchor id {}".format(path.relative_to(site), identifier))
        for value in page.resources:
            resource(path, value)
        for value in page.links:
            resource(path, value, required=False)
        for content in page.styles:
            css(path, content)
    search = site / "js" / "search-data.js"
    if not search.is_file():
        errors.append("Missing generated search data")
    else:
        text = search.read_text(encoding="utf-8").split("window.BEST_OFFLINE_SEARCH = ", 1)[1].rstrip().rstrip(";")
        entries = json.loads(text)
        for entry in entries:
            resource(site / "index.html", entry["url"], required=False)
        if not entries:
            errors.append("Empty search index")
    if errors:
        raise SystemExit("\n".join(errors))
    print("PASS: {} HTML pages, {} active stylesheets, {} search sections; no remote or missing resources.".format(
        len(pages), len(checked_css), len(entries)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("site")
    check(parser.parse_args().site)
