# Best Offline

A reusable MkDocs theme for internal documentation. Its editable override lives in **theme/**, with **base.html**, **main.html**, and local **js/**, **css/**, and **fonts/** directories.

The generated site is designed to open directly from **site/index.html**. Search works from disk without a server, JSON fetches, or browser security exceptions.

## What is included

- Read the Docs-style navigation with light and dark appearances.
- Highlight.js 11.12.0 with all 193 bundled languages, including Lua, Python, C, C++, Java, Fortran, and Bash.
- MathJax 3.2.2, including its local runtime components, using SVG output.
- Lunr 2.3.9 and a search index generated locally on each build.
- Local Inter and JetBrains Mono fonts; font data is also embedded in CSS for direct-file compatibility.
- Cards, badges, expandable explanations, and wide cheat sheets with clickable, highlighted code declarations.
- Separate Linux and Windows wheelhouses, exact dependency locks, asset licenses, and SHA-256 manifests.

See **validation/RESULTS.md** for tested versions and the exact scope of verification.

Current package release: **0.1.1**. See [CHANGELOG.md](CHANGELOG.md) and
[DEPENDENCIES.md](DEPENDENCIES.md) for updates and the reasons for retained pins.

## Install offline

Python and pip must already exist on the target machine. Copy this project with the appropriate wheelhouse.

RHEL7 x86_64 / Python 3.6:

~~~bash
python3.6 tools/install-offline.py rhel7_python36_wheelhouse .venv
source .venv/bin/activate
python -m mkdocs build --strict
~~~

RHEL9 x86_64 / Python 3.9:

~~~bash
python3.9 tools/install-offline.py rhel9_python39_wheelhouse .venv
source .venv/bin/activate
python -m mkdocs build --strict
~~~

Windows x86_64 / standard CPython 3.14:

~~~powershell
python tools/install-offline.py windows_python314_wheelhouse .venv
.\.venv\Scripts\python.exe -m mkdocs build --strict
~~~

The installer checks the interpreter, platform, architecture, and wheel hashes before creating a new environment. It uses no package index or cache, and blocks Python socket connections during installation. It refuses to overwrite an existing environment.

The Windows source compatibility target is Python 3.10+. The included Windows wheelhouse is specifically for standard CPython 3.14; other minor versions and free-threaded Python need their own wheels and validation.

Open **site/index.html** after the build. Readers need only a browser and the whole generated site directory.

## Daily editing

1. Edit Markdown under **docs/**.
2. Add new pages to **mkdocs.yml**.
3. Run **python -m mkdocs build --strict**.
4. Run **python tools/check-site.py site** to audit local links and resources.

The **Writing documentation** sidebar section contains Markdown basics, working link/image/download examples, Python/Lua/C++ highlighting examples, and a LaTeX math guide with source and rendered results. Normal editing and builds do not need npm, Node.js, a TeX installation, or internet access.

The [styled-content guide](docs/guide/styled-content.md) documents reusable CSS classes with copyable examples. The [cheat-sheet guide](docs/guide/cheat-sheets.md) explains links inside code, and the [example API reference](docs/reference/cheat-sheet.md) demonstrates the wide layout. Both light and dark mode use the same local assets.

Start new pages from **templates/api-reference.md** or **templates/runbook.md**.
The [workflow guide](docs/guide/workflow.md) covers ownership, review dates,
release checks, and environment upgrades; the [troubleshooting guide](docs/guide/troubleshooting.md)
covers missing extensions, local assets, search, and links.

For an optional preview server:

~~~bash
python -m mkdocs serve --dev-addr 127.0.0.1:8000
~~~

For a server serving existing output on Python 3.6:

~~~bash
cd site
python3.6 -m http.server 8000 --bind 127.0.0.1
~~~

## Theme overrides and reuse

The project uses the built-in Read the Docs theme as its base configuration, with all active templates and browser dependencies supplied by **theme/**:

~~~yaml
use_directory_urls: false
theme:
  name: readthedocs
  custom_dir: theme
  include_search_page: false
plugins:
  - best-offline
~~~

The companion plugin generates **js/search-data.js** and rejects common remote resource references. Keep it enabled. Do not also enable MkDocs' default search plugin for this theme.

The same directory is packaged in the **mkdocs-best-offline** wheel. Another project can use **theme.name: best_offline** without **custom_dir** after installing the wheelhouse. See the included configuration guide for the full example.

Edit **theme/css/theme.css** for layout and appearance. Highlight colors are derived from the bundled Visual Studio light/dark styles. Edit **tools/vendor-assets.cjs** when changing how third-party assets are prepared.

## Maintainer preparation

Only preparing or updating the bundle needs a connection:

~~~bash
npm ci
npm run vendor
~~~

This creates all browser runtime files inside the theme. Dependencies are pinned in **package-lock.json**; versions, licenses, and hashes are recorded in **theme/vendor-manifest.json**.

Resolve Python dependencies in an isolated environment on the actual target interpreter. The input files under **requirements/** are preparation seeds; the complete frozen dependencies live in each wheelhouse's **requirements.lock**. To update only the project's theme wheel while keeping the tested dependency set, run **python tools/refresh-theme-wheel.py WHEELHOUSE** and repeat validation.

For RHEL7, bootstrap with pip 21.3.1, setuptools 59.6.0, and wheel 0.37.1. For RHEL9/Windows, the tested bootstrap is pip 25.3, setuptools 80.9.0, and wheel 0.45.1.

~~~bash
python -m pip install -r requirements/rhel7-python36.in
python tools/package-theme.py /tmp/theme-wheel
python -m pip install --no-index --no-deps /tmp/theme-wheel/*.whl
python -m mkdocs build --strict
python tools/make-wheelhouse.py rhel7_python36_wheelhouse
~~~

Use the corresponding requirements file and wheelhouse name for other targets. Build wheels on the target OS; do not reuse Windows binary wheels on Linux.

The packaging helper uses native temporary storage before copying files back to the Windows mount. This avoids chmod/copy-metadata failures on the shared drive.

## Container verification

The pinned image definitions are under **containers/**. The Windows helper mounts the parent **offline_docs** directory at **/workspace** and runs installation and both theme modes with container networking disabled:

~~~powershell
.\tools\validate-containers.ps1 -Target rhel7
.\tools\validate-containers.ps1 -Target rhel9
~~~

Pull the pinned images once while connected; the verification helper uses **--pull=never**. Image digests are also recorded in the wheelhouse manifests.

~~~powershell
podman pull --arch amd64 registry.access.redhat.com/ubi7/python-36@sha256:592b341772926e0617dd3b4fd40354640340e1f900090a682c8c3cea64b025e1
podman pull --arch amd64 registry.access.redhat.com/ubi9/python-39@sha256:447a4c9f6ead4f063bed8778793ac9e972004e5a55d103b375de83c885887e50
~~~

For UBI7, use **/opt/rh/rh-python36/root/usr/bin/python3.6** to create a clean environment rather than the image's preactivated virtualenv.

## Browser verification

Maintainer-only checks use Playwright with Edge and Firefox. The legacy harness uses a portable Firefox 78.15 ESR and GeckoDriver 0.30.0 under **build/legacy-firefox/**. Test browsers are not needed in the offline transfer bundle.

~~~powershell
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path (Get-Location) 'build\browsers'
node node_modules/playwright/cli.js install firefox
node tools/browser-check.cjs site build/qa/final
node tools/legacy-firefox-check.cjs site
~~~

Run **.\tools\prepare-legacy-browser.ps1** once while connected to prepare the portable legacy browser on Windows.

The modern checks block and record external page requests. The legacy check uses a blocked outbound proxy and inspects resource timing. See the reports for test coverage and limitations.

## Transfer

Use **dist/best_offline-transfer.zip**, or copy this directory excluding **node_modules/**, **build/**, **.venv*/**, and other development caches. To recreate the ZIP after updating and validating:

~~~bash
python tools/make-transfer.py
~~~

Always copy the entire generated **site/** directory for readers. Keep the source, relevant wheelhouse, and tools together for authors.
