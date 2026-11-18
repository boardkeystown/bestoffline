"""Build an installable theme while keeping the override in ./theme."""
from pathlib import Path
from setuptools import setup

ROOT = Path(__file__).parent
ASSETS = [
    str(path.relative_to(ROOT / "theme")).replace("\\", "/")
    for path in (ROOT / "theme").rglob("*")
    if path.is_file() and "__pycache__" not in path.parts
    and path.suffix not in (".py", ".pyc")
]

setup(
    name="mkdocs-best-offline",
    version="0.1.0",
    description="A self-contained Read the Docs inspired MkDocs theme",
    packages=["best_offline_theme"],
    package_dir={"best_offline_theme": "theme"},
    package_data={"best_offline_theme": ASSETS},
    python_requires=">=3.6",
    install_requires=["mkdocs>=1.3.1,<2"],
    entry_points={
        "mkdocs.themes": ["best_offline=best_offline_theme"],
        "mkdocs.plugins": ["best-offline=best_offline_theme.plugin:OfflinePlugin"],
    },
)
