# Offline guarantees

Offline behavior is tested at three separate layers: package installation, documentation builds, and browser use.

## Installation

Each wheelhouse has exact versions, SHA-256 hashes, and a target manifest. The installer checks these before creating a new environment. Linux validation uses a fresh container with networking disabled.

Python and pip are prerequisites. The bundle does not install operating-system packages.

## Builds

Normal builds use the committed theme assets. They do not run npm, download fonts, or contact a CDN. The search-data JavaScript is generated from the current documentation.

~~~bash
python -m mkdocs build --strict
python tools/check-site.py site
~~~

The site checker verifies local resource paths and rejects remote resource references. Ordinary outbound hyperlinks are allowed, but their destinations are unavailable offline.

## Browser use

The theme uses classic scripts and relative HTML links. Search loads its data through a local script tag. It does not use fetch, XMLHttpRequest, workers, or service workers.

Fonts are embedded in the local stylesheet. Mathematics uses SVG output. These choices avoid common direct-file cross-origin restrictions.

Browser validation uses fresh profiles and records resource requests. Any attempted external request is a failure, even when the page appears to work.

## Compatibility boundaries

The frontend is designed for Firefox 78 ESR-era JavaScript and CSS. The validation report lists actual tested browser versions; a compilation target alone does not prove compatibility.

Storage, clipboard access, and local scripting can be restricted by browser or enterprise policy. Appearance switching still works without storage. The copy button has a legacy fallback. If local scripting is prohibited, use the optional localhost server.

The UBI images validate the RHEL userspace and interpreter, not a full RHEL desktop or kernel installation. A final smoke test on the actual offline host remains useful.

## Maintaining the bundle

Keep the source, wheelhouses, lock files, asset licenses, and validation report together. When changing the theme package, rebuild its wheel in each wheelhouse and regenerate the hashes.

Maintainer test dependencies under <code>node_modules/</code> are not needed by offline authors or readers. All browser runtime assets are already under <code>theme/</code>.
