# Troubleshooting

Run commands from the project root, where `mkdocs.yml` lives. Use the interpreter from the installed environment so MkDocs and its extensions come from the same place.

## Missing pymdownx or another Python module

`pymdownx.arithmatex` is supplied by the Python package **pymdown-extensions**. This error usually means you ran a different environment's MkDocs:

~~~text
ModuleNotFoundError: No module named 'pymdownx'
~~~

On Windows:

~~~powershell
.\.venv\Scripts\python.exe -m pip show mkdocs pymdown-extensions
.\.venv\Scripts\python.exe -m mkdocs serve
~~~

On Linux:

~~~bash
.venv/bin/python -m pip show mkdocs pymdown-extensions
.venv/bin/python -m mkdocs serve
~~~

If the environment is incomplete, use the [offline installer](installation.md) to create a fresh environment from the matching wheelhouse. Installing only MkDocs does not install every extension used by this project.

## The installer reports the wrong Python version

Wheelhouses target an exact Python minor version, operating system, and architecture. The Windows wheelhouse is for standard x86_64 CPython 3.14. It cannot install into Python 3.10, Python 3.9, or a free-threaded Python build.

Check the interpreter you are invoking:

~~~bash
python --version
python -c "import sys; print(sys.executable)"
~~~

The installer also refuses to overwrite an existing directory. Choose a new environment path when testing an update.

## Pages look unstyled or code and math do not render

Copy the entire `site/` folder, including `css/`, `js/`, `fonts/`, and other assets. An individual HTML file is not a complete site.

Run:

~~~bash
python tools/check-site.py site
~~~

If the files are present but scripts are blocked by browser policy, use the [optional localhost server](installation.md#optional-local-server). For uncolored code, check the language label against the [language guide](code-highlighting.md). For raw math delimiters, check [the math syntax](../reference/math.md) and that the arithmatex extension remains enabled.

## Search shows old pages or no results

Keep `best-offline` in the `plugins` list. Rebuild after changes to Markdown, page names, or navigation. Copy the newly generated `site/js/search-data.js` with the rest of the site.

Search is intended to work directly from disk. A local server is a fallback for organizational browser restrictions, not a normal search dependency.

## Links work on Windows but fail on Linux

Match filename capitalization exactly. Use forward slashes and relative paths. A file named `API.md` is different from `api.md` on a case-sensitive filesystem.

Use source filenames in Markdown links and output filenames in raw HTML:

~~~markdown
[Installation](installation.md)
~~~

~~~html
<a href="installation.html">Installation</a>
~~~

The [links guide](links.md) covers images, downloads, and anchors. Run the audit after building; it also checks raw HTML links.

## A cheat-sheet link jumps to the wrong entry

Check that the destination ID is unique. Duplicate `id="read-samples"` attributes make the destination ambiguous. Give overloads distinct IDs such as `read-samples-buffer` and `read-samples-file`.

Use `pre class="linked-code"` for links inside highlighted code. Normal Markdown fences display their contents literally. See [clickable cheat sheets](cheat-sheets.md).

## My new page is not in the sidebar

Add the file to `nav` in `mkdocs.yml`. Paths are relative to `docs/`. Check YAML indentation, then rebuild.

## Cards display Markdown punctuation

Use `markdown="1"` on each HTML block wrapper and keep `md_in_html` in `markdown_extensions`. See the [card examples](styled-content.md#cards-with-markdown-inside).

## A wheel or asset hash does not match

Recopy the complete validated bundle, including its manifests and lock files. A partially copied or edited wheel should not be installed by bypassing the hash check.

For an intentional maintainer change, rebuild the theme wheel and regenerate the corresponding manifests through the provided tools. Do not manually change a hash just to suppress an integrity failure.

## What to include in a problem report

Record the operating system, Python version, exact command, complete error text, browser/version, whether you opened a file or localhost URL, and the smallest page that reproduces the issue. Note whether the problem occurs in both light and dark mode.
