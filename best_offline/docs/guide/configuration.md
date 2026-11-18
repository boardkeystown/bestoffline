# Theme configuration

All editable browser assets live directly beside the theme templates.

## Local override

~~~text
theme/
  base.html
  main.html
  css/
  js/
    mathjax/
  fonts/
  img/
  licenses/
  vendor-manifest.json
~~~

This project configures the directory as an override of the built-in Read the Docs theme. Its own base template explicitly loads local assets.

~~~yaml
use_directory_urls: false
theme:
  name: readthedocs
  custom_dir: theme
plugins:
  - best-offline
~~~

The companion plugin is installed from the theme wheel. It generates the local search-data script on every build and rejects common remote-resource references.

## Use the packaged theme elsewhere

Install the matching wheelhouse, then use this configuration without copying an override directory:

~~~yaml
site_name: Internal documentation
use_directory_urls: false
theme:
  name: best_offline
plugins:
  - best-offline
markdown_extensions:
  - fenced_code
  - tables
  - admonition
  - attr_list
  - md_in_html
  - def_list
  - footnotes
  - toc:
      permalink: true
  - pymdownx.arithmatex:
      generic: true
~~~

## Appearance

Edit the CSS variables at the beginning of <code>theme/css/theme.css</code>. Light and dark mode have separate color values. Code colors are generated from Highlight.js's locally bundled Visual Studio light and dark styles.

The first visit follows the browser's system preference. The toggle saves your explicit choice when browser storage permits it. Some browsers isolate or disable storage for local files; the toggle still works on the current page.

## Fonts

Inter and JetBrains Mono files are bundled under <code>theme/fonts/</code>. The generated font stylesheet embeds the font bytes so direct-file browsing does not depend on cross-origin font permission. System fonts remain the fallback, including for glyphs outside the bundled Latin subset.

## Updating vendor assets

This is a connected maintainer operation, not part of offline authoring:

~~~bash
npm ci
npm run vendor
~~~

Pinned npm versions and integrity values live in <code>package-lock.json</code>. Generated assets, licenses, and SHA-256 hashes live in the theme directory. Rebuild and validate all wheelhouses after changing packaged theme files.

Do not paste CDN examples into the templates. Obtain the library during preparation and include the complete runtime files locally.
