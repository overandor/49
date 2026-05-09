def moat_summary(assets: list[str]) -> str:
    lines = ["# Moat / IP Summary", "", "## Candidate assets"]
    lines += [f"- {asset}" for asset in assets]
    lines += ["", "## Note", "This is not a legal opinion. Patent, copyright, tax, and securities claims require professional review."]
    return "\n".join(lines)
