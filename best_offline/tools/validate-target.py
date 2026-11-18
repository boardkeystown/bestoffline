"""Validate both the local override and installed theme without Python networking."""
import argparse
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import yaml
import mkdocs

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("output")
parser.add_argument("--expected-python", required=True)
parser.add_argument("--container-network-none", action="store_true")
args = parser.parse_args()
if "{}.{}".format(*sys.version_info[:2]) != args.expected_python:
    raise SystemExit("Wrong Python interpreter")
output = Path(args.output).resolve()
output.mkdir(parents=True, exist_ok=True)
guard = str(root / "tools" / "no-network.py")
report = {"python": platform.python_version(), "system": platform.system(), "machine": platform.machine(),
          "mkdocs": mkdocs.__version__, "python_network_blocked": True,
          "container_network_none": args.container_network_none, "checks": []}
if Path("/etc/redhat-release").exists():
    report["os_release"] = Path("/etc/redhat-release").read_text().strip()


def run(name, command):
    process = subprocess.run(command, cwd=str(root), stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                             universal_newlines=True)
    (output / (name + ".log")).write_text(process.stdout, encoding="utf-8")
    print(process.stdout)
    if process.returncode:
        raise SystemExit(process.returncode)
    report["checks"].append(name)


run("dependencies", [sys.executable, guard, "pip", "--disable-pip-version-check", "check"])
run("search-rebuild", [sys.executable, str(root / "tools" / "check-rebuild.py")])
run("override-build", [sys.executable, guard, "mkdocs", "build", "--strict", "--site-dir", str(output / "site")])
run("override-audit", [sys.executable, str(root / "tools" / "check-site.py"), str(output / "site")])
with tempfile.TemporaryDirectory(prefix="best-offline-config-") as temporary:
    config = yaml.safe_load((root / "mkdocs.yml").read_text(encoding="utf-8"))
    config["theme"] = {"name": "best_offline"}
    config["docs_dir"] = str(root / "docs")
    config_file = Path(temporary) / "mkdocs.yml"
    config_file.write_text(yaml.safe_dump(config), encoding="utf-8")
    run("packaged-build", [sys.executable, guard, "mkdocs", "build", "--strict", "-f",
                          str(config_file), "--site-dir", str(output / "packaged-site")])
    run("packaged-audit", [sys.executable, str(root / "tools" / "check-site.py"), str(output / "packaged-site")])
report["passed"] = True
(output / "validation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print("PASS: override and installed theme on Python " + platform.python_version())
