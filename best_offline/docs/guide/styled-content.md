# Cards and styled content

Use these examples directly in a Markdown page. The theme already includes the CSS, fonts, and JavaScript they need. No icon service, CDN, or additional Python package is required.

A CSS **class** is the name inside `class="..."`. Classes such as `feature-card` are reusable styles supplied by this theme; they are not built-in Markdown syntax.

## Cards with Markdown inside

**Write this:**

~~~~html
<div class="feature-grid" markdown="1">

<div class="feature-card" markdown="1">
<div class="card-icon" aria-hidden="true">01 / WRITE</div>

### Write a page

Use **Markdown** for your documentation.

[Open the writing guide](authoring.md).

</div>

<div class="feature-card" markdown="1">
<div class="card-icon" aria-hidden="true">02 / LINK</div>

### Connect your pages

Link to a page, a heading, or a local download.

[See link examples](links.md).

</div>

</div>
~~~~

**Result:**

<div class="feature-grid" markdown="1">

<div class="feature-card" markdown="1">
<div class="card-icon" aria-hidden="true">01 / WRITE</div>

### Write a page

Use **Markdown** for your documentation.

[Open the writing guide](authoring.md).

</div>

<div class="feature-card" markdown="1">
<div class="card-icon" aria-hidden="true">02 / LINK</div>

### Connect your pages

Link to a page, a heading, or a local download.

[See link examples](links.md).

</div>

</div>

The grid uses two columns and becomes one column on small screens. Add more `feature-card` elements for more cards. A card also works by itself without the grid.

Keep blank lines around Markdown paragraphs and headings. Put `markdown="1"` on **each block wrapper** containing Markdown, including both the grid and each card. The project enables the standard `md_in_html` extension in `mkdocs.yml`. If you move these examples into another project, copy that setting too.

Without `markdown="1"`, write the contents as HTML instead:

~~~html
<div class="feature-card">
  <div class="card-icon" aria-hidden="true">&lt;/&gt;</div>
  <h3>Code examples</h3>
  <p>Read the <a href="code-highlighting.html">code guide</a>.</p>
</div>
~~~

Markdown links use source paths such as `code-highlighting.md`. Raw HTML links use the **built path**, such as `code-highlighting.html`, because MkDocs does not rewrite raw HTML links. Both are relative to the current page.

## Icons without a download

The class is `card-icon`, singular. It provides accent color and monospace styling; it is not an icon library and does not automatically choose an image.

Use a short label such as `01 / API`, an ASCII symbol such as `&lt;/&gt;`, a local SVG image, or an inline SVG. Text and local SVGs have no network dependency. Emoji appearance depends on the fonts installed on the reader's machine.

~~~html
<div class="card-icon" aria-hidden="true">&lt;/&gt;</div>
~~~

Use `aria-hidden="true"` only for decoration when the nearby heading already conveys its meaning. Give meaningful images an appropriate `alt` description.

## Eyebrows and introductory text

**Write this:**

~~~html
<p class="eyebrow">QUICK REFERENCE</p>
<p class="intro">Commands, examples, and explanations for your team.</p>
~~~

**Result:**

<p class="eyebrow">QUICK REFERENCE</p>
<p class="intro">Commands, examples, and explanations for your team.</p>

`eyebrow` creates a small accent label; `intro` creates a larger, muted introduction.

## Badges

**Write this:**

~~~html
<div class="platforms">
  <span>Python 3.6</span>
  <span>Linux</span>
  <span>Windows</span>
</div>
~~~

**Result:**

<div class="platforms"><span>Python 3.6</span><span>Linux</span><span>Windows</span></div>

Despite its name, `platforms` can hold any short labels: versions, platforms, file types, or status. These badges are text, not buttons.

## Expandable explanations

**Write this:**

~~~~html
<details class="disclosure" markdown="1">
<summary>Why keep the whole site folder?</summary>

The HTML pages depend on the nearby **styles, scripts, fonts, and search data**.

- Copy the entire folder.
- Open its `index.html` file.

</details>
~~~~

**Result:**

<details class="disclosure" markdown="1">
<summary>Why keep the whole site folder?</summary>

The HTML pages depend on the nearby **styles, scripts, fonts, and search data**.

- Copy the entire folder.
- Open its `index.html` file.

</details>

Add `open` to the opening tag to start expanded. This is native HTML and works without JavaScript. Keep sections that are link destinations outside closed disclosures so readers can see the target immediately.

## Notes, shortcuts, highlights, and definitions

These use extensions already enabled in this project or ordinary HTML:

~~~~markdown
!!! note "A useful detail"
    Explain something the reader needs.

!!! tip "A shortcut"
    Press <kbd>/</kbd> to search.

!!! warning "Before rebuilding"
    Edit the source Markdown, not generated HTML.

Use <mark>highlighted text</mark> sparingly.

Wheelhouse
:   A folder of Python wheels for installation without a package index.

An explanatory footnote.[^example]

[^example]: Put supporting detail here.
~~~~

!!! tip "A shortcut"
    Press <kbd>/</kbd> to search.

Use <mark>highlighted text</mark> sparingly.

The [components gallery](../reference/components.md) includes more rendered examples. Notes use the theme's accent color, tips use green, and warnings use amber.

## Reusable class reference

| Class or setting | Apply to | Result |
| --- | --- | --- |
| `feature-grid` | Container around cards | Two-column responsive card grid |
| `feature-card` | Each card container | Bordered card with compact headings and paragraphs |
| `card-icon` | Decorative label inside a card | Accent color and monospace text |
| `eyebrow` | Short paragraph | Small, spaced accent label |
| `intro` | Introductory paragraph | Larger, muted introduction |
| `platforms` | Container of `span` elements | Wrapping row of small badges |
| `disclosure` | `details` with a `summary` | Expandable explanation box |
| `linked-code` | `pre` containing `code` | Preserve clickable links while highlighting code |
| `language-python`, `language-lua`, `language-cpp`, etc. | `code` inside `pre` | Choose the Highlight.js language |
| `cheatsheet-grid` | Container around API groups | Responsive, dense reference grid |
| `api-group` | Group containing an `h2` and code block | Bordered module with an accent heading |
| `api-green`, `api-purple`, `api-orange` | Same element as `api-group` | Optional group accent; default is blue |
| `wide: true` | YAML metadata at the top of a page | Expand the reading area and hide the right-hand table of contents |
| `sr-only` | Text for assistive technology | Hide visually while keeping it available to screen readers |

The theme generates `admonition`, `admonition-title`, `headerlink`, `code-toolbar`, `with-toolbar`, `hljs-*`, and `arithmatex` automatically. Use the documented Markdown syntax instead of assembling these classes yourself. Sidebar, search, breadcrumb, pagination, and theme-toggle classes belong to the page layout.

## Add your own styles

Edit `theme/css/theme.css` for reusable theme components. For a project-specific stylesheet, create `docs/styles/extra.css` and register it:

~~~yaml
extra_css:
  - styles/extra.css
~~~

Use the theme variables so your styles follow light and dark mode:

~~~css
.my-panel {
  background: var(--surface);
  color: var(--text);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  padding: 16px;
}
~~~

Available variables are `--bg`, `--surface`, `--sidebar`, `--hover`, `--text`, `--muted`, `--border`, `--accent`, `--accent-soft`, `--code`, `--green`, `--shadow`, `--sans`, and `--mono`. API groups additionally use `--group-color`.

Keep fonts, images, imports, and scripts local. Build and check your work with `python -m mkdocs build --strict` and `python tools/check-site.py site`.

For a dense reference page with links inside highlighted code, continue to [clickable cheat sheets](cheat-sheets.md).
