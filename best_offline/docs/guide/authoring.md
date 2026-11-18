# Writing documentation

Write your content in Markdown files under <code>docs/</code>. MkDocs combines those files with the theme to produce the HTML files under <code>site/</code>.

This walkthrough uses the configuration already included in this project. Start with the [offline installation guide](installation.md) if you have not installed its Python environment.

## Create a page

Create <code>docs/guide/first-page.md</code> in your text editor and paste this example:

~~~~markdown
# My first page

This page explains how our measurement tool works.

## Before you begin

- Install the tool.
- Have a sample input file ready.

## Run the tool

Use the command below:

~~~bash
python measure.py samples.csv
~~~

## Related documentation

See the [installation guide](installation.md).
~~~~

The example command is illustrative; replace it with the command for your own tool. A level-one heading supplies the page title. Level-two and level-three headings divide the page into sections and appear in the page's table of contents.

## Add the page to the sidebar

Open <code>mkdocs.yml</code>. Add your new file to the existing <code>nav</code> list:

~~~yaml
nav:
  - Overview: index.md
  - Writing documentation:
      - Markdown basics: guide/authoring.md
      - My first page: guide/first-page.md
~~~

Merge the new entry into your current navigation rather than replacing all its existing entries. Paths in <code>nav</code> start at <code>docs/</code>, so use <code>guide/first-page.md</code>, not <code>docs/guide/first-page.md</code>. Use spaces for YAML indentation.

## Headings and paragraphs

**Write this:**

~~~markdown
# Page title

The first paragraph introduces the topic.

This is a second paragraph, separated by a blank line.

## Main section

Explain one part of the topic here.

### A smaller section

Add supporting detail here.
~~~

Use one <code>#</code> heading per page, then <code>##</code> and <code>###</code> for its structure. A blank line starts a new paragraph; a single newline usually continues the same paragraph.

## Emphasis and inline code

**Write this:**

~~~markdown
Use **bold** for a key instruction and *italics* for emphasis.
The setting `use_directory_urls: false` keeps file links portable.
~~~

**Result:**

Use **bold** for a key instruction and *italics* for emphasis.
The setting <code>use_directory_urls: false</code> keeps file links portable.

Single backticks mark short commands, paths, or identifiers as inline code. For multiple lines, use the fenced blocks shown in the [code highlighting guide](code-highlighting.md).

## Lists

**Write this:**

~~~markdown
Required files:

- Source documentation
- Theme files
- Matching Python wheelhouse

Build procedure:

1. Activate the Python environment.
2. Build the documentation.
3. Open the generated homepage.
~~~

**Result:**

Required files:

- Source documentation
- Theme files
- Matching Python wheelhouse

Build procedure:

1. Activate the Python environment.
2. Build the documentation.
3. Open the generated homepage.

## Tables

**Write this:**

~~~markdown
| Setting | Value | Purpose |
| --- | --- | --- |
| use_directory_urls | false | Explicit HTML filenames |
| custom_dir | theme | Load our local theme override |
~~~

**Result:**

| Setting | Value | Purpose |
| --- | --- | --- |
| use_directory_urls | false | Explicit HTML filenames |
| custom_dir | theme | Load our local theme override |

## Notes and warnings

Admonitions start with three exclamation marks. Indent their contents by four spaces.

**Write this:**

~~~markdown
!!! note "Before you begin"
    Select the wheelhouse that matches your operating system and Python version.

!!! tip "Keep the whole site"
    Copy the entire generated site directory when sharing documentation.
~~~

**Result:**

!!! note "Before you begin"
    Select the wheelhouse that matches your operating system and Python version.

!!! tip "Keep the whole site"
    Copy the entire generated site directory when sharing documentation.

Use <code>warning</code> in place of <code>note</code> for a warning box.

## Preview and rebuild

From the project root, with its Python environment active:

~~~bash
python -m mkdocs serve --dev-addr 127.0.0.1:8000
~~~

Open <code>http://127.0.0.1:8000/</code> to preview edits. Stop the server with Ctrl+C.

For the portable output:

~~~bash
python -m mkdocs build --strict
python tools/check-site.py site
~~~

Open <code>site/index.html</code>. Rebuild whenever you change Markdown or the navigation; the search data updates with the build.

On Windows, you can call the environment directly without activating it:

~~~powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe tools/check-site.py site
~~~

Edit the Markdown source, not the generated HTML: the next build replaces generated pages.

## Continue with examples

- [Links, images, and downloads](links.md): paths, heading anchors, and working local examples.
- [Code highlighting](code-highlighting.md): Markdown fences and Python, Lua, and C++ examples.
- [Cards and styled content](styled-content.md): copyable cards, icons, badges, expandable sections, and every reusable CSS class.
- [Clickable cheat sheets](cheat-sheets.md): links inside highlighted code and a wide, grouped API reference.
- [LaTeX mathematics](../reference/math.md): the source and rendered result for common formulas.
- [Components](../reference/components.md): additional notes, tables, definitions, and footnotes.

Optional online reference: [MkDocs authoring documentation](https://www.mkdocs.org/user-guide/writing-your-docs/). Everything needed for these examples is already in this project.
