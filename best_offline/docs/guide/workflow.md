# Workflow and page templates

The most useful additions to a documentation site are consistent pages, clear ownership, and an easy way to verify a release. The theme already supplies the presentation; use these habits to keep the content useful.

## Start from a template

Two editable Markdown templates are included in the project:

| Template | Use it for |
| --- | --- |
| `templates/api-reference.md` | A linked overview, function contract, parameters, return values, errors, and examples |
| `templates/runbook.md` | A repeatable task with prerequisites, numbered steps, expected results, and recovery |

From the project root on Windows:

~~~powershell
Copy-Item templates/api-reference.md docs/reference/my-api.md
Copy-Item templates/runbook.md docs/guide/my-procedure.md
~~~

On Linux:

~~~bash
cp templates/api-reference.md docs/reference/my-api.md
cp templates/runbook.md docs/guide/my-procedure.md
~~~

Replace the example content, then add each new file to `nav` in `mkdocs.yml`. The files in `templates/` are authoring inputs; MkDocs only builds them after you copy them under `docs/`.

## Make responsibility and scope visible

Add a small table near the beginning of an important page:

~~~markdown
| Document information | Value |
| --- | --- |
| Owner | Instrumentation team |
| Applies to | Capture service 2.x |
| Status | Reviewed |
| Last reviewed | YYYY-MM-DD |
~~~

Use the date of the actual content review, not the last build date. Record software versions, operating systems, hardware revisions, and units wherever they affect the instructions.

A table is visible without theme customization. Arbitrary YAML metadata such as `owner` is not displayed automatically. The theme's documented `wide: true` setting is different: it explicitly controls the page layout.

## Organize for both scanning and learning

Keep the overview compact. Put contracts, examples, and failure cases in the detail sections beneath it.

- Use a stable explicit ID such as `{ #read-samples }` for every public entry.
- Link function names in the overview to those IDs.
- Document parameter units, valid ranges, buffer sizes, ownership, and lifetimes.
- State return values and error behavior, including empty or invalid inputs.
- Show one minimal successful call and one realistic failure case.
- Include searchable words in prose; an image of a table or formula contributes no searchable text.

The [clickable cheat-sheet guide](cheat-sheets.md) shows how to preserve links inside highlighted code. The site audit rejects missing destinations and duplicate IDs, which become easy to introduce on a long API page.

## Keep examples and diagrams portable

Store screenshots, diagrams, and downloads under `docs/`. For diagrams, a locally exported SVG or PNG is a simple choice that already works with this theme. Retain the editable diagram source alongside your documentation project.

If you later want diagrams generated from text, prepare and test their renderer locally before enabling it. A plugin name alone does not guarantee that it avoids a CDN.

Prefer actual text over screenshots of code. Readers can select it, search it, copy it, and follow links inside it. The [math guide](../reference/math.md) covers searchable LaTeX source with local rendering.

## Separate theme maintenance from your content

For a large internal documentation collection, consider a separate content repository using the installed `best_offline` theme. Keep the reusable theme, its examples, and its wheelhouses in this project. That makes it easier to update the theme without mixing changes into your internal pages.

The [configuration guide](configuration.md#use-the-packaged-theme-elsewhere) shows the installed-theme setup. If you prefer editing the local override, keep your own CSS changes small and documented.

## Before sharing a documentation release

From the project root, in the installed environment:

~~~bash
python -m mkdocs build --strict
python tools/check-site.py site
~~~

On Windows without activating the environment:

~~~powershell
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe tools/check-site.py site
~~~

Then:

1. Open `site/index.html` directly from disk.
2. Try search, a code-copy button, a math equation, and several deep links.
3. Check both light and dark mode on the oldest required browser.
4. Copy the complete `site/` folder to another directory and open it again.
5. Give the release a version or date and retain the matching source commit.

Readers need the complete site folder. Authors need the source, theme, tools, and the correct wheelhouse as well.

## Updating an offline authoring environment

Normal content edits need no dependency upgrades. For a new validated bundle, create a new environment alongside the old one:

~~~powershell
python tools/install-offline.py windows_python314_wheelhouse .venv-next
.\.venv-next\Scripts\python.exe -m mkdocs build --strict
.\.venv-next\Scripts\python.exe tools/check-site.py site
~~~

For RHEL7, use `python3.6` and `rhel7_python36_wheelhouse`; for RHEL9 use `python3.9` and `rhel9_python39_wheelhouse`. Their environment interpreter is `.venv-next/bin/python`.

Switch your editor or shell to the new environment after verification. Keep the previous bundle and environment until the new one works on the real target machine. Do not move an existing virtual environment between machines.

Connected maintainers can run `python tools/check-updates.py` to compare pins against official package registries. It only writes a report and does not install anything. The project-root `DEPENDENCIES.md` explains retained versions and upgrade policy.
