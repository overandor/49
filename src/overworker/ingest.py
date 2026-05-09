from __future__ import annotations

from pathlib import Path
from overworker.config import settings


def read_text_file(path: str | Path) -> str:
    p = Path(path)
    if p.stat().st_size > settings.max_file_bytes:
        raise ValueError(f"File too large for MVP ingest: {p}")
    return p.read_text(errors="replace")


def list_ingestable_files(root: str | Path) -> list[Path]:
    base = Path(root)
    ignored = {".git", "node_modules", "__pycache__", ".venv"}
    return [p for p in base.rglob("*") if p.is_file() and not any(part in ignored for part in p.parts)]
