"""Connected maintainer step, after a successful build in the target Python."""
import argparse
from email.parser import Parser
import hashlib
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import zipfile

parser = argparse.ArgumentParser()
parser.add_argument("destination")
parser.add_argument("--image", default="")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
final_destination = Path(args.destination).resolve()
final_destination.mkdir(parents=True, exist_ok=True)
scratch = tempfile.TemporaryDirectory(prefix="best-offline-wheels-")
destination = Path(scratch.name)
subprocess.check_call([sys.executable, str(root / "tools" / "package-theme.py"), str(destination)])
theme_wheel = next(destination.glob("mkdocs_best_offline-*.whl"))
subprocess.check_call([sys.executable, "-m", "pip", "--disable-pip-version-check", "install",
                       "--no-index", "--no-deps", "--force-reinstall", str(theme_wheel)])
installed = json.loads(subprocess.check_output(
    [sys.executable, "-m", "pip", "--disable-pip-version-check", "list", "--format=json"],
    universal_newlines=True))
requirements = "\n".join("{}=={}".format(item["name"], item["version"]) for item in installed) + "\n"
with tempfile.TemporaryDirectory(prefix="best-offline-resolve-") as temporary:
    requirements_path = Path(temporary) / "resolved.txt"
    requirements_path.write_text(requirements, encoding="utf-8")
    subprocess.check_call([
        sys.executable, "-m", "pip", "--disable-pip-version-check", "download",
        "--no-cache-dir", "--only-binary=:all:", "--dest", str(destination),
        "--find-links", str(destination), "-r", str(requirements_path),
    ])
manifest = {
    "python": "{}.{}".format(*sys.version_info[:2]),
    "python_full": platform.python_version(),
    "system": platform.system(),
    "machine": platform.machine(),
    "implementation": platform.python_implementation(),
    "image": args.image,
    "wheels": [],
}
lines = []
bootstrap = []
for wheel in sorted(destination.glob("*.whl")):
    digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
    with zipfile.ZipFile(str(wheel)) as archive:
        metadata_path = next(name for name in archive.namelist() if name.endswith(".dist-info/METADATA"))
        metadata = Parser().parsestr(archive.read(metadata_path).decode("utf-8"))
    line = "{}=={} --hash=sha256:{}".format(metadata["Name"], metadata["Version"], digest)
    lines.append(line)
    if metadata["Name"].lower() in ("pip", "setuptools", "wheel"):
        bootstrap.append(line)
    manifest["wheels"].append({"file": wheel.name, "sha256": digest, "name": metadata["Name"], "version": metadata["Version"]})
(destination / "requirements.lock").write_text("\n".join(lines) + "\n", encoding="utf-8")
(destination / "bootstrap.lock").write_text("\n".join(bootstrap) + "\n", encoding="utf-8")
(destination / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Locked {} wheels for {} Python {}".format(len(lines), manifest["system"], manifest["python"]))
for path in destination.iterdir():
    if path.is_file():
        shutil.copyfile(str(path), str(final_destination / path.name))
# Remove only replaced wheel files after the complete new set has been copied.
# Leaving an older version here would make the verified installer reject it.
new_wheels = {path.name for path in destination.glob("*.whl")}
for previous in final_destination.glob("*.whl"):
    if previous.name not in new_wheels:
        previous.unlink()
scratch.cleanup()
