"""Collect passing evidence and hash the source used for the transfer bundle."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--release", required=True, help="Release identifier used in build/qa output directories.")
args = parser.parse_args()
if not args.release or any(character not in "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ.-" for character in args.release):
    raise SystemExit("Release identifier must contain only letters, digits, dots, or hyphens.")
prefix = "release-" + args.release
destination = root / "validation"
destination.mkdir(exist_ok=True)
reports = {
    prefix + "-rhel7-build.json": "build/verified-rhel7/validation.json",
    prefix + "-rhel9-build.json": "build/verified-rhel9/validation.json",
    prefix + "-windows-build.json": "build/" + prefix + "-windows/validation.json",
    prefix + "-browsers.json": "build/qa/" + prefix + "/browser-report.json",
    prefix + "-firefox78.json": "build/qa/" + prefix + "-firefox78/browser-report.json",
}
for name, source in reports.items():
    record = json.loads((root / source).read_text(encoding="utf-8"))
    if not record.get("passed"):
        raise SystemExit("Validation has not passed: " + source)
    shutil.copyfile(str(root / source), str(destination / name))
for name in ("rhel7", "rhel9", "windows"):
    folder = prefix + "-windows" if name == "windows" else "verified-" + name
    for path in (root / "build" / folder).glob("*.log"):
        shutil.copyfile(str(path), str(destination / (prefix + "-" + name + "-" + path.name)))
sources = [root / name for name in ("README.md", "DEPENDENCIES.md", "CHANGELOG.md", "THIRD_PARTY.md",
                                    "mkdocs.yml", "setup.py", "MANIFEST.in", "package.json", "package-lock.json")]
for directory in ("theme", "docs", "templates", "tools", "requirements", "containers"):
    sources.extend(path for path in (root / directory).rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts and path.suffix != ".pyc")
hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(sources)}
(destination / (prefix + "-source-sha256.json")).write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
print("Collected {} passing reports and {} source hashes".format(len(reports), len(hashes)))
