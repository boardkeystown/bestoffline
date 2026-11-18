# Dependency review — 2026-11-18

This project prioritizes reproducible offline installation, Python 3.6 support,
and Firefox 78 compatibility. “Reviewed” does not mean every package is the
newest upstream release.

## Updated in 0.1.1

| Component | Previous | Now | Target |
| --- | --- | --- | --- |
| Highlight.js | 11.11.1 | 11.12.0 | All browsers; 193 bundled languages |
| PyYAML | 6.0 | 6.0.1 | RHEL7 / Python 3.6 |
| watchdog | 2.1.9 | 2.3.1 | RHEL7 / Python 3.6 |
| Markdown | 3.7 | 3.9 | RHEL9 and Windows |
| PyMdown Extensions | 10.14.3 | 10.21.3 | RHEL9 and Windows |

The Python updates were resolved and downloaded inside their actual target
interpreter/platform. The project theme is now version 0.1.1 in all wheelhouses.

## Deliberately retained versions

| Component | Retained | Upstream at review | Reason |
| --- | --- | --- | --- |
| MkDocs on RHEL7 | 1.3.1 | 1.6.1 | Newer MkDocs requires a newer Python than 3.6 |
| Markdown on RHEL7 | 3.3.7 | 3.11.3 | Python 3.6 compatibility |
| PyMdown on RHEL7 | 9.1 | 13.1 | Python 3.6 compatibility |
| MkDocs on RHEL9/Windows | 1.6.1 | 1.6.1 | Current upstream version |
| Markdown on RHEL9/Windows | 3.9 | 3.11.3 | Shared Python 3.9-compatible baseline, also within the Windows 3.10+ source target |
| PyMdown on RHEL9/Windows | 10.21.3 | 13.1 | Shared Python 3.9-compatible baseline |
| MathJax | 3.2.2 | 4.1.3 | Version 4 changes component/font loading; migration needs a dedicated file-mode and Firefox 78 review |
| Lunr | 2.3.9 | 2.3.9 | Current upstream version |
| Inter / JetBrains Mono font packages | 5.3.0 | 5.3.0 | Current upstream versions |
| esbuild | 0.25.12 | 0.28.2 | Maintainer-only, pinned asset-generation tool |
| Playwright | 1.56.1 | 1.65.1 | Maintainer-only, pinned browser-test tool |

The pip/setuptools/wheel bootstrap pins also remain unchanged. RHEL7 retains
21.3.1 / 59.6.0 / 0.37.1. RHEL9 and Windows retain
25.3 / 80.9.0 / 0.45.1. Newer bootstrap versions are available for the latter
targets; upgrading the installer toolchain is separate from rendering docs.
These tools are not loaded by the generated site.

The Windows wheelhouse still targets standard CPython 3.14 specifically.
Supporting the source on Python 3.10+ does not make CPython 3.14 binary wheels
usable on those other interpreters.

## Repeat the review

On a connected maintainer machine, from the project root:

~~~bash
python tools/check-updates.py
npm outdated
npm audit
~~~

The Python command writes **validation/dependency-status.json** using official
PyPI and npm metadata. It checks every external wheelhouse package and direct
npm dependency. It changes no pins and installs nothing. A
**python_metadata_candidate** only satisfies the interpreter version metadata;
it still needs actual wheels, dependency resolution, and target validation.

The npm advisory query reported zero known vulnerabilities in the checked npm
dependency graph. That is a registry result, not a general security certification
or an audit of the Python dependencies. The retained dependency set and npm
result are recorded in **validation/dependency-status.json** and
**validation/npm-audit.json**.

Do not run update tools as part of an offline documentation build. Normal
authoring consumes the already prepared assets and wheels.

## Prepare and validate changes

1. Review upstream release notes and the required Python/browser versions.
2. Prepare Python changes in an isolated environment on each actual target.
3. Build the docs before freezing a replacement wheelhouse.
4. If browser libraries change, rebuild the local assets with **npm run vendor**.
5. Bump the theme package version for distributed theme changes and refresh all
   three theme wheels.
6. Repeat fresh offline installations, strict builds, resource audits, and browser
   checks. Include actual Firefox 78, direct-file mode, and linked code/math.
7. Update the dependency review, changelog, validation evidence, and transfer ZIP.
8. Keep the prior release available until the new bundle works on the offline host.

For theme-only changes, **tools/refresh-theme-wheel.py** preserves the existing
dependency versions. For dependency changes, **tools/make-wheelhouse.py** freezes
the isolated environment and removes replaced wheel files from the destination.
Use a clean environment; the tool includes every installed Python distribution.

## Upstream references

- [MkDocs releases](https://www.mkdocs.org/about/release-notes/)
- [Python-Markdown changelog](https://python-markdown.github.io/changelog/)
- [PyMdown Extensions changelog](https://facelessuser.github.io/pymdown-extensions/about/changelog/)
- [Highlight.js releases](https://github.com/highlightjs/highlight.js/releases)
- [MathJax 4 migration changes](https://docs.mathjax.org/en/latest/upgrading/whats-new-4.0.html)

The machine-readable report contains the individual registry source for each
package. The validation results describe the tests actually performed.

For release 0.1.1, Windows validation output is under
**build/release-0.1.1-windows/**, modern-browser output under
**build/qa/release-0.1.1/**, and legacy-browser output under
**build/qa/release-0.1.1-firefox78/**. After those checks pass, run
**python tools/collect-validation.py --release 0.1.1** to collect their reports
alongside the current **build/verified-rhel7/** and **build/verified-rhel9/** logs.
