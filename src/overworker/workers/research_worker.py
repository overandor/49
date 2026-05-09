def summarize_findings(items: list[str]) -> str:
    return "# Research Findings\n\n" + "\n".join(f"- {item}" for item in items)
