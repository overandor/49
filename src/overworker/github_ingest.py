from __future__ import annotations

import re
from dataclasses import dataclass, asdict
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse

import httpx


@dataclass
class GitHubIngestResult:
    owner: str
    repo: str
    branch: str
    files_written: list[str]
    skipped_files: list[str]
    root_path: str

    def to_dict(self) -> dict:
        return asdict(self)


GITHUB_RE = re.compile(r"github\.com[:/](?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+)(?:\.git)?")
TEXT_EXTENSIONS = {
    ".md", ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".toml", ".yml", ".yaml",
    ".txt", ".css", ".html", ".sh", ".env.example", ".dockerfile"
}
TEXT_FILENAMES = {"README", "README.md", "LICENSE", "Dockerfile", "Makefile", ".gitignore"}


def parse_github_url(url: str) -> tuple[str, str]:
    match = GITHUB_RE.search(url)
    if not match:
        raise ValueError("Expected GitHub URL like https://github.com/owner/repo")
    repo = match.group("repo")
    if repo.endswith(".git"):
        repo = repo[:-4]
    return match.group("owner"), repo


def is_supported_text_file(path: str) -> bool:
    name = Path(path).name
    suffix = Path(path).suffix.lower()
    return name in TEXT_FILENAMES or suffix in TEXT_EXTENSIONS


async def fetch_public_repo(url: str, target_dir: str | Path, max_files: int = 120, max_file_bytes: int = 200_000) -> GitHubIngestResult:
    owner, repo = parse_github_url(url)
    root = Path(target_dir)
    root.mkdir(parents=True, exist_ok=True)
    api = f"https://api.github.com/repos/{owner}/{repo}"

    async with httpx.AsyncClient(timeout=20, follow_redirects=True) as client:
        meta_resp = await client.get(api)
        if meta_resp.status_code >= 400:
            raise RuntimeError(f"GitHub metadata fetch failed: HTTP {meta_resp.status_code}")
        meta = meta_resp.json()
        branch = meta.get("default_branch") or "main"
        tree_url = f"{api}/git/trees/{branch}?recursive=1"
        tree_resp = await client.get(tree_url)
        if tree_resp.status_code >= 400:
            raise RuntimeError(f"GitHub tree fetch failed: HTTP {tree_resp.status_code}")
        tree = tree_resp.json().get("tree", [])

        files_written: list[str] = []
        skipped_files: list[str] = []
        for item in tree:
            if len(files_written) >= max_files:
                skipped_files.append("max_file_limit_reached")
                break
            if item.get("type") != "blob":
                continue
            path = item.get("path", "")
            size = int(item.get("size") or 0)
            if not is_supported_text_file(path) or size > max_file_bytes:
                skipped_files.append(path)
                continue
            raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
            raw = await client.get(raw_url)
            if raw.status_code >= 400:
                skipped_files.append(path)
                continue
            out = root / path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(raw.text, errors="replace")
            files_written.append(path)

    return GitHubIngestResult(owner=owner, repo=repo, branch=branch, files_written=files_written, skipped_files=skipped_files, root_path=str(root))
