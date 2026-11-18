# Offline installation

Copy the project and the wheelhouse matching the target interpreter and operating system. Python and pip must already be installed.

## Choose the correct wheelhouse

| Machine | Interpreter | Directory |
| --- | --- | --- |
| RHEL7 x86_64 | Python 3.6 | rhel7_python36_wheelhouse |
| RHEL9 x86_64 | Python 3.9 | rhel9_python39_wheelhouse |
| Windows x86_64 | Standard CPython 3.14 | windows_python314_wheelhouse |

The theme targets Python 3.10+ on Windows; each Python version still needs its own compatible wheelhouse. A CPython 3.14 wheelhouse is not a promise of installation on Python 3.10 or a free-threaded interpreter.

## Install in a separate environment

From the project root on RHEL7:

~~~bash
python3.6 tools/install-offline.py rhel7_python36_wheelhouse .venv
source .venv/bin/activate
python -m mkdocs build --strict
~~~

On RHEL9:

~~~bash
python3.9 tools/install-offline.py rhel9_python39_wheelhouse .venv
source .venv/bin/activate
python -m mkdocs build --strict
~~~

On Windows, use a standard Python interpreter:

~~~powershell
python tools/install-offline.py windows_python314_wheelhouse .venv
.\.venv\Scripts\python.exe -m mkdocs build --strict
~~~

The installer verifies every wheel's SHA-256 hash and target compatibility, creates a new environment, and installs with indexes and caches disabled. It refuses to overwrite an existing environment.

!!! note "The UBI7 Python image"
    Its default Python command belongs to a preactivated virtual environment. For a clean install inside that image, use the underlying interpreter at <code>/opt/rh/rh-python36/root/usr/bin/python3.6</code>.

## Read the finished site

Open <code>site/index.html</code>. Navigation, search, code coloring, and mathematics are designed to work directly from disk. Copy the entire <code>site/</code> directory when sharing it.

Readers do not need Python, pip, MkDocs, Node.js, or a TeX installation.

## Optional local server

If organizational browser policy restricts local scripts, start a server bound only to your own computer:

~~~bash
python -m http.server 8000 --bind 127.0.0.1 --directory site
~~~

Python 3.6 does not support the <code>--directory</code> option. Use:

~~~bash
cd site
python3.6 -m http.server 8000 --bind 127.0.0.1
~~~

Then open <code>http://127.0.0.1:8000/</code>. Stop the server with Ctrl+C.

## Rebuild after editing

~~~bash
python -m mkdocs build --strict
python tools/check-site.py site
~~~

No online asset preparation is involved in a normal rebuild. See [writing documentation](authoring.md) for the editing workflow.
