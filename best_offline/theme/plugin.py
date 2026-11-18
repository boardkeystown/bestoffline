"""Python 3.6-compatible search data and offline resource checks."""
import json
import os
from html.parser import HTMLParser
from urllib.parse import urlsplit

from mkdocs.plugins import BasePlugin
from mkdocs.exceptions import ConfigurationError


def remote(value):
    return value.startswith("//") or urlsplit(value).scheme.lower() in ("http", "https")


class Sections(HTMLParser):
    def __init__(self, title, url):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.page_title = title
        self.url = url
        self.title = title
        self.anchor = ""
        self.parts = []
        self.entries = []
        self.heading = None
        self.heading_parts = []
        self.skipping = 0
        self.remote_assets = []

    def flush(self):
        content = " ".join(" ".join(self.parts).split())
        if content or self.anchor:
            self.entries.append({
                "title": self.title,
                "page": self.page_title,
                "url": self.url + ("#" + self.anchor if self.anchor else ""),
                "text": content,
            })
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("script", "style"):
            self.skipping += 1
        for key in ("src", "poster"):
            if attrs.get(key) and remote(attrs[key]):
                self.remote_assets.append(attrs[key])
        if tag == "link" and remote(attrs.get("href", "")):
            self.remote_assets.append(attrs["href"])
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.flush()
            self.heading = tag
            self.anchor = attrs.get("id", "")
            self.heading_parts = []
        if tag in ("p", "br", "li", "pre", "td", "th"):
            self.parts.append(" ")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.skipping:
            self.skipping -= 1
        if tag == self.heading:
            self.title = " ".join(self.heading_parts).strip().rstrip("\u00b6").strip()
            self.heading = None
        if tag in ("p", "li", "pre", "td", "th"):
            self.parts.append(" ")

    def handle_data(self, data):
        if self.skipping:
            return
        if self.heading:
            self.heading_parts.append(data)
        else:
            self.parts.append(data)


class OfflinePlugin(BasePlugin):
    def on_pre_build(self, config):
        # mkdocs serve reuses the plugin between builds.
        self.entries = []

    def on_config(self, config):
        self.entries = []
        if config.get("use_directory_urls", True):
            raise ConfigurationError(
                "best-offline requires use_directory_urls: false for direct-file navigation."
            )
        for key in ("extra_css", "extra_javascript"):
            for asset in config.get(key, []):
                path = getattr(asset, "path", asset)
                if remote(str(path)):
                    raise ConfigurationError("Offline asset must be local: " + str(path))
        return config

    def on_page_content(self, html, page, config, files):
        parser = Sections(page.title, page.url)
        parser.feed(html)
        parser.flush()
        if parser.remote_assets:
            raise ConfigurationError(
                "Remote resource in {}: {}".format(page.file.src_path, parser.remote_assets[0])
            )
        self.entries.extend(parser.entries)
        return html

    def on_post_build(self, config):
        path = os.path.join(config["site_dir"], "js", "search-data.js")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        for index, entry in enumerate(self.entries):
            entry["id"] = str(index)
        data = json.dumps(self.entries, ensure_ascii=True, separators=(",", ":"))
        with open(path, "w", encoding="utf-8", newline="\n") as stream:
            stream.write("/* Generated locally by mkdocs-best-offline. */\n")
            stream.write("window.BEST_OFFLINE_SEARCH = " + data + ";\n")
