from __future__ import annotations


def route_worker(task: str) -> str:
    text = task.lower()
    if any(x in text for x in ["readme", "docs", "documentation"]):
        return "docs_worker"
    if any(x in text for x in ["investor", "pitch", "funding", "one-pager"]):
        return "investor_worker"
    if any(x in text for x in ["ip", "moat", "proprietary", "asset"]):
        return "ip_worker"
    if any(x in text for x in ["risk", "disclaimer", "compliance"]):
        return "risk_worker"
    if any(x in text for x in ["code", "test", "compile", "repo"]):
        return "repo_cleanup_worker"
    return "research_worker"
