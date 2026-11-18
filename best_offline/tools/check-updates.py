"""Connected maintainer report; never installs packages or changes version pins."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

from packaging.specifiers import SpecifierSet
from packaging.version import InvalidVersion, Version


ROOT = Path(__file__).resolve().parent.parent


def get_json(url):
    request = Request(url, headers={"User-Agent": "best-offline-dependency-review/1.0"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def canonical(name):
    return name.lower().replace("_", "-")


def python_candidate(releases, python):
    candidates = []
    for version, files in releases.items():
        try:
            parsed = Version(version)
        except InvalidVersion:
            continue
        if parsed.is_prerelease or parsed.is_devrelease:
            continue
        # This checks Python metadata, not wheel tags or the dependency graph.
        if any(not item.get("yanked") and
               SpecifierSet(item.get("requires_python") or "").contains(python)
               for item in files):
            candidates.append(parsed)
    return str(max(candidates)) if candidates else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="validation/dependency-status.json")
    args = parser.parse_args()
    manifests = {}
    names = set()
    for folder in sorted(ROOT.glob("*_wheelhouse")):
        manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
        manifests[folder.name] = manifest
        names.update(canonical(item["name"]) for item in manifest["wheels"]
                     if canonical(item["name"]) != "mkdocs-best-offline")
    npm = json.loads((ROOT / "package.json").read_text(encoding="utf-8"))["devDependencies"]
    requests = [("python", name, "https://pypi.org/pypi/{}/json".format(quote(name, safe=""))) for name in sorted(names)]
    requests += [("npm", name, "https://registry.npmjs.org/{}/latest".format(quote(name, safe=""))) for name in sorted(npm)]
    data, errors = {}, []
    with ThreadPoolExecutor(max_workers=6) as pool:
        futures = [(kind, name, url, pool.submit(get_json, url)) for kind, name, url in requests]
        for kind, name, url, future in futures:
            try:
                data[(kind, name)] = future.result()
            except Exception as error:
                errors.append({"package": name, "source": url, "error": str(error)})
    report = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Release metadata only; not a vulnerability audit. Python candidates are not resolved or wheel/platform validated.",
        "python": {},
        "npm": [],
        "errors": errors,
    }
    for folder, manifest in manifests.items():
        records = []
        for item in manifest["wheels"]:
            name = canonical(item["name"])
            if name == "mkdocs-best-offline" or ("python", name) not in data:
                continue
            upstream = data[("python", name)]
            candidate = python_candidate(upstream["releases"], manifest["python_full"])
            records.append({
                "name": name, "pinned": item["version"],
                "latest": upstream["info"]["version"],
                "latest_requires_python": upstream["info"].get("requires_python"),
                "python_metadata_candidate": candidate,
                "candidate_newer_than_pin": bool(candidate and Version(candidate) > Version(item["version"])),
                "source": "https://pypi.org/project/{}/".format(name),
            })
        report["python"][folder] = {"python": manifest["python_full"], "packages": records}
    for name, pinned in sorted(npm.items()):
        if ("npm", name) in data:
            upstream = data[("npm", name)]
            report["npm"].append({
                "name": name, "pinned": pinned, "latest": upstream["version"],
                "source": "https://registry.npmjs.org/{}/latest".format(quote(name, safe="")),
            })
    destination = Path(args.output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for folder, target in report["python"].items():
        updates = [item for item in target["packages"] if item["candidate_newer_than_pin"]]
        print("{}: {} newer Python-metadata candidates".format(folder, len(updates)))
        for item in updates:
            print("  {}: {} -> {}".format(item["name"], item["pinned"], item["python_metadata_candidate"]))
    for item in report["npm"]:
        if item["pinned"] != item["latest"]:
            print("npm {}: {} -> {}".format(item["name"], item["pinned"], item["latest"]))
    print("Report: " + str(destination))
    if errors:
        raise SystemExit("Some registry checks failed; see the report.")


if __name__ == "__main__":
    main()
