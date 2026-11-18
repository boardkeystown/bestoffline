# Best Offline

A local-first MkDocs theme for internal documentation on RHEL7 / Python 3.6,
RHEL9 / Python 3.9, and Windows. The project lives in [best_offline/](best_offline/).

- Light and dark modes with Read the Docs-style navigation.
- Local Highlight.js, MathJax, Lunr search, and fonts; no CDN dependencies.
- Direct-file reading and search: open the generated `site/index.html`.
- Cards, expandable explanations, and a wide cheat-sheet layout with clickable,
  syntax-highlighted function declarations.
- Python wheelhouses with pinned versions and hashes for the three tested targets.

Start with the [installation and maintenance instructions](best_offline/README.md),
the [authoring guide](best_offline/docs/guide/authoring.md), or the
[validation results](best_offline/validation/RESULTS.md).

Release **0.1.1** adds page templates, troubleshooting, and compatible dependency
updates. See the [dependency review](best_offline/DEPENDENCIES.md) for the versions
that intentionally remain pinned for older targets.

## Windows quick start

From this repository's root, using standard x86_64 CPython 3.14:

~~~powershell
cd best_offline
python tools/install-offline.py windows_python314_wheelhouse .venv
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe tools/check-site.py site
~~~

Open `best_offline/site/index.html` from the repository root. For subsequent
editing, run `.\.venv\Scripts\python.exe -m mkdocs serve` inside `best_offline/`.
The installer creates a new environment; skip installation if that environment
already exists. Other Windows Python versions need their own wheelhouse.

Linux installation commands and the disconnected UBI7/UBI9 container checks are
in the [project README](best_offline/README.md).

## What belongs in Git

The source, editable theme, local browser dependencies, licenses, wheelhouses,
locks, and selected validation evidence are tracked intentionally. A complete
clone can be copied into an offline environment without downloading Python or
browser dependencies; Python must already be installed.

Generated sites, transfer ZIPs, build folders, downloaded test browsers, virtual
environments, npm dependencies, caches, editor settings, and local credentials
are ignored. Rebuild the site locally; run `python tools/make-transfer.py` inside
`best_offline/` to prepare the transfer archive.

Git preserves file bytes through `.gitattributes` because the offline validation
tools check SHA-256 hashes. Third-party notices are in
[THIRD_PARTY.md](best_offline/THIRD_PARTY.md) and `best_offline/theme/licenses/`.
