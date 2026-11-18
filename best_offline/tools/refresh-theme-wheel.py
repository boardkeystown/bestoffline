"""Replace only this project's wheel and update its locked hash in a wheelhouse."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("wheelhouse")
args = parser.parse_args()
wheelhouse = Path(args.wheelhouse).resolve()
subprocess.check_call([sys.executable, str(root / "tools" / "package-theme.py"), str(wheelhouse)])
wheel = next(wheelhouse.glob("mkdocs_best_offline-*.whl"))
digest = hashlib.sha256(wheel.read_bytes()).hexdigest()
manifest = json.loads((wheelhouse / "manifest.json").read_text(encoding="utf-8"))
for entry in manifest["wheels"]:
    if entry["name"].lower().replace("_", "-") == "mkdocs-best-offline":
        entry["file"] = wheel.name
        entry["sha256"] = digest
        requirement = entry["name"] + "==" + entry["version"] + " --hash=sha256:" + digest
        break
else:
    raise SystemExit("Theme is missing from the wheelhouse manifest")
lock = wheelhouse / "requirements.lock"
lines = lock.read_text(encoding="utf-8").splitlines()
lines = [requirement if line.lower().startswith(("mkdocs-best-offline==", "mkdocs_best_offline==")) else line for line in lines]
lock.write_text("\n".join(lines) + "\n", encoding="utf-8")
(wheelhouse / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print("Updated theme wheel and hash: " + wheel.name)
