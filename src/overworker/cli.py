from __future__ import annotations

import json
from pathlib import Path
import typer
from rich.console import Console

from overworker.repo_scanner import scan_repo
from overworker.verification.firewall import verify_project
from overworker.scoring.overwork_score import score_project
from overworker.export.markdown_exporter import render_report, write_report

app = typer.Typer(help="Overworker: turn messy technical projects into verified deliverable packages.")
console = Console()


@app.command()
def scan(path: str, out: str = "out/overworker-report") -> None:
    """Scan a local repo/path and export a readiness report."""
    scan_result = scan_repo(path)
    verification = verify_project(scan_result)
    score = score_project(scan_result, verification)

    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    (out_dir / "scan.json").write_text(json.dumps(scan_result.to_dict(), indent=2))
    (out_dir / "verification-report.json").write_text(json.dumps(verification.to_dict(), indent=2))
    (out_dir / "overwork-score.json").write_text(json.dumps(score.to_dict(), indent=2))
    report = render_report(scan_result, verification, score)
    write_report(out_dir / "sample-report.md", report)

    console.print(f"[green]Overworker report exported to {out_dir}[/green]")
    console.print(score.to_dict())


@app.command()
def score(path: str) -> None:
    """Print only the Overwork Score for a local repo/path."""
    scan_result = scan_repo(path)
    verification = verify_project(scan_result)
    score_result = score_project(scan_result, verification)
    console.print_json(json.dumps(score_result.to_dict()))


if __name__ == "__main__":
    app()
