"""Collect passing evidence and hash the source used for the transfer bundle."""
import hashlib
import json
from pathlib import Path
import shutil

root = Path(__file__).resolve().parent.parent
destination = root / "validation"
destination.mkdir(exist_ok=True)
reports = {
    "styled-rhel7-build.json": "build/verified-rhel7/validation.json",
    "styled-rhel9-build.json": "build/verified-rhel9/validation.json",
    "styled-windows-build.json": "build/styled-windows/validation.json",
    "styled-windows-browsers.json": "build/qa/styled-windows/browser-report.json",
    "styled-rhel7-firefox78.json": "build/qa/styled-firefox78/browser-report.json",
    "styled-transfer-browsers.json": "build/qa/styled-transfer/browser-report.json",
}
for name, source in reports.items():
    record = json.loads((root / source).read_text(encoding="utf-8"))
    if not record.get("passed"):
        raise SystemExit("Validation has not passed: " + source)
    shutil.copyfile(str(root / source), str(destination / name))
for name in ("rhel7", "rhel9", "windows"):
    folder = "styled-windows" if name == "windows" else "verified-" + name
    for path in (root / "build" / folder).glob("*.log"):
        shutil.copyfile(str(path), str(destination / ("styled-" + name + "-" + path.name)))
sources = [root / name for name in ("mkdocs.yml", "setup.py", "MANIFEST.in", "package.json", "package-lock.json")]
for directory in ("theme", "docs", "tools", "requirements", "containers"):
    sources.extend(path for path in (root / directory).rglob("*") if path.is_file()
                   and "__pycache__" not in path.parts and path.suffix != ".pyc")
hashes = {path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sorted(sources)}
(destination / "styled-source-sha256.json").write_text(json.dumps(hashes, indent=2) + "\n", encoding="utf-8")
print("Collected {} passing reports and {} source hashes".format(len(reports), len(hashes)))
