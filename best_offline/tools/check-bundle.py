"""Validate source/asset/wheel integrity and installer rejection behavior."""
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import sys
import tempfile
import zipfile

root = Path(__file__).resolve().parent.parent
vendor = json.loads((root / "theme" / "vendor-manifest.json").read_text(encoding="utf-8"))
for name, digest in vendor["files"].items():
    assert hashlib.sha256((root / "theme" / name).read_bytes()).hexdigest() == digest, name
source = {path.relative_to(root / "theme").as_posix(): path.read_bytes()
          for path in (root / "theme").rglob("*")
          if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"}
for name in ("rhel7_python36_wheelhouse", "rhel9_python39_wheelhouse", "windows_python314_wheelhouse"):
    directory = root / name
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    assert {item["file"] for item in manifest["wheels"]} == {p.name for p in directory.glob("*.whl")}
    lock = (directory / "requirements.lock").read_text(encoding="utf-8")
    for item in manifest["wheels"]:
        assert hashlib.sha256((directory / item["file"]).read_bytes()).hexdigest() == item["sha256"]
        assert "--hash=sha256:" + item["sha256"] in lock
    with zipfile.ZipFile(str(next(directory.glob("mkdocs_best_offline-*.whl")))) as archive:
        for file, content in source.items():
            assert archive.read("best_offline_theme/" + file) == content, name + ": " + file
    print("PASS: {} ({} wheels), packaged theme matches source".format(name, len(manifest["wheels"])))

spec = importlib.util.spec_from_file_location("installer", str(root / "tools" / "install-offline.py"))
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
with tempfile.TemporaryDirectory(prefix="best-offline-negative-") as temporary:
    directory = Path(temporary) / "wheelhouse"
    directory.mkdir()
    (directory / "example.whl").write_bytes(b"corrupted")
    manifest = {"python": "{}.{}".format(*sys.version_info[:2]), "system": platform.system(),
                "machine": platform.machine(), "implementation": platform.python_implementation(),
                "wheels": [{"file": "example.whl", "sha256": "0" * 64}]}
    (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    environment = Path(temporary) / "environment"
    try:
        installer.install(str(directory), str(environment))
    except SystemExit as error:
        assert "integrity check failed" in str(error), str(error)
    else:
        raise AssertionError("Corrupted wheel accepted")
    assert not environment.exists(), "Environment created before integrity check"
    manifest["python"] = "0.0"
    (directory / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    try:
        installer.install(str(directory), str(environment))
    except SystemExit as error:
        assert "Wheelhouse targets" in str(error), str(error)
    else:
        raise AssertionError("Wrong interpreter accepted")
print("PASS: {} vendor hashes; corrupt wheels and wrong interpreters rejected before writes".format(len(vendor["files"])))
