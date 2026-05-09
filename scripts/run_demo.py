#!/usr/bin/env python3
from pathlib import Path
from overworker.repo_scanner import scan_repo
from overworker.verification.firewall import verify_project
from overworker.scoring.overwork_score import score_project
from overworker.export.markdown_exporter import render_report, write_report

root = Path('.')
out = Path('out/demo')
out.mkdir(parents=True, exist_ok=True)
scan = scan_repo(root)
verification = verify_project(scan)
score = score_project(scan, verification)
write_report(out / 'sample-report.md', render_report(scan, verification, score))
print(f'Demo report written to {out / "sample-report.md"}')
