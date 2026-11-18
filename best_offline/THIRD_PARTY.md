# Bundled third-party software

Browser runtime files are copied or built from exact npm package versions. Their original license texts are under **theme/licenses/**. The complete asset hash inventory and source package names are in **theme/vendor-manifest.json**.

| Software | Version | License |
| --- | --- | --- |
| Highlight.js | 11.11.1 | BSD-3-Clause |
| Lunr | 2.3.9 | MIT |
| MathJax | 3.2.2 | Apache-2.0 |
| Inter font package | 5.3.0 | SIL Open Font License |
| JetBrains Mono font package | 5.3.0 | SIL Open Font License |

Highlight styles are adapted by adding light/dark scope selectors. Original **vs.css** and **vs2015.css** are retained beside the generated stylesheet.

The font files are retained as WOFF2 files and embedded as data URLs in the generated font stylesheet.

The local override uses MkDocs' built-in Read the Docs theme configuration. MkDocs and its bundled theme retain their upstream notices in the distributed MkDocs wheel and installed package. Python package licenses remain inside their respective wheels.

The original templates, layout CSS, and support code in this project are separate from the vendored libraries. Development tools and test browsers are excluded from the transfer archive.
