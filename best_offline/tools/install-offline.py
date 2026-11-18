"""Install a verified target wheelhouse without using the network (Python 3.6+)."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import sysconfig
import venv


def install(wheelhouse, destination):
    wheelhouse = Path(wheelhouse).resolve()
    destination = Path(destination).resolve()
    manifest = json.loads((wheelhouse / "manifest.json").read_text(encoding="utf-8"))
    version = "{}.{}".format(*sys.version_info[:2])
    if version != manifest["python"] or platform.system() != manifest["system"]:
        raise SystemExit("Wheelhouse targets {} Python {}; running {} Python {}.".format(
            manifest["system"], manifest["python"], platform.system(), version))
    aliases = {"amd64": "x86_64", "x64": "x86_64"}
    machine = platform.machine().lower()
    target_machine = manifest["machine"].lower()
    if aliases.get(machine, machine) != aliases.get(target_machine, target_machine):
        raise SystemExit("Wheelhouse architecture mismatch.")
    if platform.python_implementation() != manifest["implementation"]:
        raise SystemExit("Wheelhouse Python implementation mismatch.")
    if sysconfig.get_config_var("Py_GIL_DISABLED"):
        raise SystemExit("This wheelhouse targets standard CPython, not a free-threaded build.")
    expected_files = set(item["file"] for item in manifest["wheels"])
    if expected_files != set(path.name for path in wheelhouse.glob("*.whl")):
        raise SystemExit("Wheelhouse has missing or extra wheels; regenerate its manifest.")
    for item in manifest["wheels"]:
        path = wheelhouse / item["file"]
        if path.parent != wheelhouse or hashlib.sha256(path.read_bytes()).hexdigest() != item["sha256"]:
            raise SystemExit("Wheel integrity check failed: " + item["file"])
    if destination.exists():
        raise SystemExit("Refusing to overwrite existing environment: " + str(destination))
    # with_pip=False also works around RHEL's ensurepip / preactivated virtualenv quirks.
    venv.EnvBuilder(with_pip=False).create(str(destination))
    python = destination / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    pip_wheel = next(wheelhouse.glob("pip-*.whl"))
    environment = dict(os.environ)
    for name in list(environment):
        if name.startswith("PIP_") or name in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV"):
            environment.pop(name, None)
    environment["PYTHONPATH"] = str(pip_wheel)
    environment["PIP_CONFIG_FILE"] = os.devnull
    environment["PIP_NO_INDEX"] = "1"
    guard = str(Path(__file__).resolve().parent / "no-network.py")
    command = [str(python), guard, "pip", "--disable-pip-version-check", "install",
               "--no-index", "--no-cache-dir", "--only-binary=:all:", "--require-hashes",
               "--find-links", str(wheelhouse)]
    subprocess.check_call(command + ["-r", str(wheelhouse / "bootstrap.lock")], env=environment)
    environment.pop("PYTHONPATH")
    subprocess.check_call(command + ["-r", str(wheelhouse / "requirements.lock")], env=environment)
    subprocess.check_call([str(python), guard, "pip", "--disable-pip-version-check", "check"], env=environment)
    print("Offline installation complete: " + str(python))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("wheelhouse")
    parser.add_argument("environment")
    args = parser.parse_args()
    install(args.wheelhouse, args.environment)
