from __future__ import annotations

from pathlib import Path
from .models import ProjectScan

PACKAGE_FILES = {
    "pyproject.toml", "package.json", "requirements.txt", "Dockerfile",
    "docker-compose.yml", "setup.py", "go.mod", "Cargo.toml"
}
ENTRYPOINT_NAMES = {"main.py", "app.py", "cli.py", "index.js", "server.js"}


def scan_repo(path: str | Path) -> ProjectScan:
    root = Path(path)
    if not root.exists():
        raise FileNotFoundError(f"Project path not found: {root}")

    files = [str(p.relative_to(root)) for p in root.rglob("*") if p.is_file() and ".git" not in p.parts]
    lower = {f.lower() for f in files}

    package_files = [f for f in files if Path(f).name in PACKAGE_FILES]
    entrypoints = [f for f in files if Path(f).name in ENTRYPOINT_NAMES]

    return ProjectScan(
        root=str(root),
        files=files,
        readme_found=any(Path(f).name.lower().startswith("readme") for f in files),
        tests_found=any("test" in Path(f).name.lower() or f.startswith("tests/") for f in files),
        license_found=any(Path(f).name.lower() == "license" for f in files),
        package_files=package_files,
        entrypoints=entrypoints,
    )
