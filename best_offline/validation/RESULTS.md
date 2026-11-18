# Validation results

Validated on 2026-11-18. The included JSON reports contain exact interpreter, OS, and browser versions.

## Current: release 0.1.1

The compatible dependency updates in **../DEPENDENCIES.md** passed fresh offline
installations and strict override/installed-theme builds on UBI7/Python 3.6.9,
UBI9/Python 3.9.25, and Windows/Python 3.14.6. Linux containers used
**--network none**; Windows installation/build commands used the Python socket
guard. The wheel counts remain 23, 24, and 22 respectively.

Every target passed dependency checks, search rebuilds, three anchor-audit
regression fixtures, and output audits covering 16 HTML pages, three active
stylesheets, and 149 searchable sections. All packaged theme files match the
source; all 122 vendored asset hashes and all wheelhouse hashes match.

Edge 157 and Firefox 142 passed the full browser suite on a copy of the site in a
different directory containing a space, in both file and localhost modes.
Checks include all 193 Highlight.js language registrations, required language
samples, links inside highlighted code, plain-text copying, code links without
JavaScript, math, search, appearance, and mobile layout. No external requests
or browser errors occurred. Actual Firefox 78.15 ESR passed direct-file checks
on the RHEL7-built output.

Both new page templates were also copied into a standalone MkDocs configuration
and passed a strict installed-theme build and link/resource audit on Windows.
An isolated theme-refresh fixture verified a 0.1.0-to-0.1.1 version bump, updated
hashes, removal of the old wheel, and preservation of unrelated pins. The bundle
audit also checks every wheel's embedded package name/version against its
manifest and exact lock entry.

Current reports are **release-0.1.1-rhel7-build.json**,
**release-0.1.1-rhel9-build.json**, **release-0.1.1-windows-build.json**,
**release-0.1.1-browsers.json**, and **release-0.1.1-firefox78.json**.
Matching logs and **release-0.1.1-source-sha256.json** record the evidence and
source snapshot. The registry review and npm advisory result are separate
reports; see **../DEPENDENCIES.md** for their scope.

The older reports below are retained as history.

## Previous: styled content and clickable cheat sheets

Removed the sidebar availability label, header slogan, and bottom branding.
Added authoring guides for cards, CSS classes, badges, disclosures, and linked
code; a wide API cheat sheet; and highlighting that preserves HTML code links.
The standard Markdown-in-HTML extension is enabled without adding dependencies.

Fresh offline installations passed on UBI7/Python 3.6.9, UBI9/Python 3.9.25,
and Windows/Python 3.14.6. Each target passed dependency checks, search rebuilds,
strict override and installed-theme builds, and local resource/link audits.
Both containers ran with networking disabled; Windows used the Python socket
guard. The audits covered 14 HTML pages, three active stylesheets, and 130 search
sections. All three theme wheels were refreshed and their source contents and
hash locks verified. All 122 vendored asset hashes still match.

Edge 157 and Firefox 142 checked all pages in direct-file and localhost modes.
Checks include rendered Markdown inside cards, disclosures, twelve linked API
declarations, keyboard navigation, links spanning several syntax tokens, escaped
C++ characters, exact plain-text copying, links with JavaScript disabled, wide
and mobile layouts, search, theme persistence, and 22 math expressions on the
math guide. There were no external requests or browser errors.

Actual Firefox 78.15 ESR checked the RHEL7 output directly from disk, including
cards, disclosures, linked highlighted declarations, escaped C++, math, and
search. Browser checks ran on Windows, not on a RHEL desktop.

The final site was copied to a different directory containing a space and passed
the complete modern-browser checks again. Updated light and dark previews are
included, along with cheat-sheet screenshots.

Current evidence is in **styled-rhel7-build.json**, **styled-rhel9-build.json**,
**styled-windows-build.json**, **styled-windows-browsers.json**,
**styled-rhel7-firefox78.json**, and **styled-transfer-browsers.json**. The
**styled-*.log** files contain build/audit output. **styled-source-sha256.json**
records the source snapshot collected for this update.

The sections and unprefixed reports below preserve earlier validation history.

## Authoring guide update

The documentation now includes a Markdown walkthrough, links/images/downloads guide, a code highlighting guide with Python/Lua/C++ source and rendered examples, and an expanded LaTeX mathematics tutorial.

The updated site passed strict builds and resource audits on Windows Python 3.14.6 and disconnected UBI7 Python 3.6.9: 11 HTML pages, three active stylesheets, and 89 search sections. UBI7 also passed installed-theme mode and the search rebuild check.

Edge checked the four authoring pages directly from disk, including the local image, heading links, cross-page links, highlighted Python/Lua/C++ blocks, 22 rendered math expressions, and mobile page width. No external requests or browser errors occurred. Firefox 78 ESR checked the expanded Markdown and mathematics pages from the RHEL7 build using the existing legacy-browser workflow.

See **authoring-browser.json**, **authoring-firefox78.json**, **authoring-rhel7-build.json**, and **authoring-rhel7-audit.log**. The updated documentation/configuration hashes are in **authoring-source-sha256.json**. The theme package, bundled assets, and Python wheelhouses are unchanged.

The sections below record the initial theme release's validation. Its **source-sha256.json**, browser reports, page counts, and transfer relocation check describe the initial documentation payload.

## Installation and builds

| Target | Python | MkDocs | Wheels | Result |
| --- | --- | --- | --- | --- |
| UBI7 / RHEL 7.9, x86_64 | 3.6.9 | 1.3.1 | 23 | Passed |
| UBI9 / RHEL 9.9, x86_64 | 3.9.25 | 1.6.1 | 24 | Passed |
| Windows, AMD64, standard CPython | 3.14.6 | 1.6.1 | 22 | Passed |

Both Linux targets were installed into fresh environments in fresh containers running with **--network none**. Python socket connections and DNS were also blocked during installation and builds. Windows used a fresh environment, no package index/cache, and the Python socket guard; the Windows machine's networking was not globally disabled.

Each target passed dependency checking, a strict build using the local theme override, and a strict build using only the installed theme package. Every output passed the local resource audit: nine HTML pages, three active stylesheets, and 63 search sections with no missing or remote resources.

The same MkDocs configuration was built twice after editing a page. The second search index contained the new content and no stale or duplicate entries.

All 122 vendored asset hashes match. All three packaged theme wheels contain the same 134 source and asset files as the theme directory. Every wheel hash matches its manifest and lock file. A corrupt-wheel fixture and a wrong-interpreter fixture were both rejected before any environment was created.

## Browser behavior

| Browser on Windows | Direct-file mode | Localhost mode |
| --- | --- | --- |
| Edge 157.0.4341.60 | Passed | Passed |
| Firefox 142.0.1 | Passed | Passed |
| Firefox 78.15.0 ESR | Passed | Not separately tested |

The final RHEL7-built output and Windows-built output were tested. RHEL9's generated HTML and search-data script match the Windows output byte for byte.

Modern-browser checks used fresh profiles and blocked/recorded external page requests. There were zero external requests, failed resources, or browser errors. Checks covered:

- All nine pages and nested navigation.
- Requested language examples, including both Fortran samples, and 192 registered language definitions.
- Ten MathJax expressions, SVG output, and resolved equation references.
- Direct-file search result navigation, empty results, plural queries, C++, and prefix matching.
- Light/dark switching and persistence after reload.
- Desktop and mobile layout without horizontal page overflow.

The actual Firefox 78 ESR check used a portable browser with outbound traffic directed to an unavailable local proxy. All nine pages loaded directly from disk, the required language samples had highlighted tokens, equations rendered, nested search links worked, dark mode worked, and no HTTP(S) page resources appeared in resource timing.

Screenshots were inspected in light and dark mode, including the legacy browser's code gallery.

The transfer ZIP was unpacked into a different directory whose path contains a space. Its relocated site passed the complete Edge and Firefox 142 checks in both direct-file and localhost modes. The final archive's site files match that tested copy byte for byte.

## Scope

The UBI tests verify RHEL userspace and interpreter compatibility on Podman's Linux VM. Browser tests ran on Windows; an actual RHEL desktop/browser deployment was not available. Enterprise policies that prohibit local scripting may require the optional localhost server.

The Windows wheelhouse is for standard CPython 3.14, not all Python 3.10+ versions or free-threaded Python. Other Windows interpreters need their own resolved wheels and validation.

Syntax coloring is provided by Highlight.js with Visual Studio-inspired palettes; its token classification is not identical to VS Code's semantic highlighting. Math support is MathJax's TeX mathematics syntax, not a full LaTeX document compiler.
