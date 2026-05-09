from __future__ import annotations

from pathlib import Path
import zipfile


def export_zip(source_dir: str | Path, zip_path: str | Path) -> Path:
    src = Path(source_dir)
    out = Path(zip_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in src.rglob("*"):
            if p.is_file():
                zf.write(p, p.relative_to(src))
    return out
