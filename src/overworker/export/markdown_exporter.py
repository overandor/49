from __future__ import annotations

from pathlib import Path
from overworker.models import ProjectScan, VerificationResult, OverworkScore


def render_report(scan: ProjectScan, verification: VerificationResult, score: OverworkScore) -> str:
    return f"""# Overworker Project Report

## Source

`{scan.root}`

## Summary

- Files detected: {len(scan.files)}
- README found: {scan.readme_found}
- License found: {scan.license_found}
- Tests found: {scan.tests_found}
- Package files: {', '.join(scan.package_files) or 'none'}
- Entrypoints: {', '.join(scan.entrypoints) or 'none'}

## Overwork Score

- Final score: {score.final_score():.2f}
- State: {score.state()}
- Weakest component: {score.weakest_component()}

## Verification

Passed: {verification.passed}

### Checks

""" + "\n".join(f"- {k}: {v}" for k, v in verification.checks.items()) + "\n\n## Warnings\n\n" + "\n".join(f"- {w}" for w in verification.warnings) + "\n\n## Next actions\n\n" + "\n".join(f"- {a}" for a in verification.next_actions) + "\n"


def write_report(path: str | Path, report: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(report)
    return out
