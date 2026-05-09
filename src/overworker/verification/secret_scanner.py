from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path


SECRET_PATTERNS = {
    "generic_api_key": re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    "openai_key": re.compile(r"sk-[A-Za-z0-9]{20,}"),
    "private_key": re.compile(r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


@dataclass
class SecretFinding:
    path: str
    kind: str
    line: int
    preview: str

    def to_dict(self) -> dict:
        return asdict(self)


def scan_text_for_secrets(text: str, path: str = "<memory>") -> list[SecretFinding]:
    findings: list[SecretFinding] = []
    for idx, line in enumerate(text.splitlines(), start=1):
        for kind, pattern in SECRET_PATTERNS.items():
            if pattern.search(line):
                preview = line[:12] + "...[redacted]"
                findings.append(SecretFinding(path=path, kind=kind, line=idx, preview=preview))
    return findings


def scan_path_for_secrets(root: str | Path) -> list[dict]:
    base = Path(root)
    findings: list[SecretFinding] = []
    ignored = {".git", "node_modules", ".venv", "__pycache__"}
    for p in base.rglob("*"):
        if not p.is_file() or any(part in ignored for part in p.parts):
            continue
        try:
            text = p.read_text(errors="replace")
        except Exception:
            continue
        findings.extend(scan_text_for_secrets(text, str(p.relative_to(base))))
    return [f.to_dict() for f in findings]
