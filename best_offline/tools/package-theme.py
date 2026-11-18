"""Build on a native temporary filesystem; write only the wheel to the share."""
import argparse
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument("destination")
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
destination = Path(args.destination).resolve()
destination.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix="best-offline-package-") as temporary:
    source = Path(temporary)
    for name in ("setup.py", "MANIFEST.in"):
        shutil.copyfile(str(root / name), str(source / name))
    shutil.copytree(str(root / "theme"), str(source / "theme"),
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
                    copy_function=shutil.copyfile)
    subprocess.check_call([
        sys.executable, "-m", "pip", "--disable-pip-version-check",
        "wheel", "--no-deps", "--no-build-isolation", "--no-cache-dir",
        "--wheel-dir", str(source / "wheels"), str(source),
    ], cwd=temporary)
    for wheel in (source / "wheels").glob("*.whl"):
        shutil.copyfile(str(wheel), str(destination / wheel.name))
