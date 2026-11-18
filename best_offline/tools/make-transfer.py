"""Create a portable bundle from an explicit allowlist, excluding caches."""
import hashlib
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent.parent
destination = root / "dist"
destination.mkdir(exist_ok=True)
archive_path = destination / "best_offline-transfer.zip"
directories = [
    "docs", "theme", "tools", "templates", "requirements", "containers", "validation", "site",
    "rhel7_python36_wheelhouse", "rhel9_python39_wheelhouse", "windows_python314_wheelhouse",
]
files = ["README.md", "THIRD_PARTY.md", "DEPENDENCIES.md", "CHANGELOG.md", "mkdocs.yml", "setup.py", "MANIFEST.in",
         "package.json", "package-lock.json"]
paths = [root / file for file in files]
for name in directories:
    directory = root / name
    if not directory.is_dir():
        raise SystemExit("Required bundle directory missing: " + name)
    paths.extend(path for path in directory.rglob("*") if path.is_file()
                 and "__pycache__" not in path.parts and path.suffix != ".pyc")
with zipfile.ZipFile(str(archive_path), "w", zipfile.ZIP_DEFLATED) as archive:
    for path in sorted(paths):
        archive.write(str(path), "best_offline/" + path.relative_to(root).as_posix())
with zipfile.ZipFile(str(archive_path)) as archive:
    if archive.testzip() is not None:
        raise SystemExit("Archive integrity verification failed")
digest = hashlib.sha256(archive_path.read_bytes()).hexdigest()
(destination / "best_offline-transfer.zip.sha256").write_text(
    digest + "  " + archive_path.name + "\n", encoding="utf-8")
print("{}: {} files, {:.1f} MiB, SHA-256 {}".format(
    archive_path, len(paths), archive_path.stat().st_size / 1048576, digest))
