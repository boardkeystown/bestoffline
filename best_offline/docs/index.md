<p class="eyebrow">LOCAL BY DESIGN</p>

# Good documentation.<br>Anywhere you work. { data-toc-label="Overview" }

<p class="intro">A familiar home for your team's knowledge. Write in Markdown, build with MkDocs, and take the entire experience with you—even when there is no connection.</p>

<div class="platforms"><span>RHEL 7 · Python 3.6</span><span>RHEL 9 · Python 3.9</span><span>Windows · Python 3.10+</span></div>

<div class="feature-grid">
  <div class="feature-card"><div class="card-icon">01 / LOCAL</div><h3>Everything travels with you</h3><p>Scripts, styles, fonts, and search data live alongside your pages. Open index.html and start reading.</p></div>
  <div class="feature-card"><div class="card-icon">02 / CODE</div><h3>A home for every language</h3><p>Bundled Highlight.js brings Lua, Python, C++, Fortran, Bash, and more into familiar light and dark palettes.</p></div>
  <div class="feature-card"><div class="card-icon">03 / MATH</div><h3>Make the reasoning visible</h3><p>Typeset equations, matrices, and derivations with a local copy of MathJax. No TeX installation needed.</p></div>
  <div class="feature-card"><div class="card-icon">04 / SEARCH</div><h3>Find it without a connection</h3><p>Search headings and content directly from disk. Your queries stay in your browser.</p></div>
</div>

## Start with your first page

Create a Markdown file under <code>docs/</code>, add it to the navigation, and rebuild.

~~~bash
python -m mkdocs build --strict
# Open site/index.html in your browser.
~~~

Your source stays simple. The theme handles navigation, code coloring, mathematics, and search.

!!! tip "Taking this into an offline environment?"
    Begin with the [offline installation guide](guide/installation.md). It explains which wheelhouse to copy and how to install without contacting a package repository.

## Explore the essentials

| Start here | What you will find |
| --- | --- |
| [Writing documentation](guide/authoring.md) | Pages, links, code blocks, and everyday editing |
| [Links, images, and downloads](guide/links.md) | Working relative links, heading anchors, and local files |
| [Code highlighting](guide/code-highlighting.md) | Copyable Markdown and Python, Lua, and C++ examples |
| [Cards and styled content](guide/styled-content.md) | Cards, icons, badges, disclosures, and reusable CSS classes |
| [Clickable cheat sheets](guide/cheat-sheets.md) | Linked code declarations and a wide API reference layout |
| [Language gallery](reference/languages.md) | Examples across the required languages |
| [LaTeX mathematics](reference/math.md) | Source syntax and rendered equations, matrices, and references |
| [Theme configuration](guide/configuration.md) | Local overrides, assets, and reusable packaging |
| [Offline guarantees](reference/offline.md) | What is bundled, what is tested, and how to verify it |

## A small example

Put an implementation beside its equation:

~~~python
def mean(values):
    """Return the arithmetic mean of a nonempty sequence."""
    return sum(values) / len(values)
~~~


~~~lua
---@class foobar
local Foobar = {}
function Foobar.new() 
    local o = {}
    return o
end
Foobar.new()
~~~

$$
\bar{x} = \frac{1}{n}\sum_{i=1}^{n} x_i
$$

Use the sidebar to explore, press <kbd>/</kbd> to search, or switch the appearance at the bottom of the navigation.
