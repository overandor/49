from __future__ import annotations

from overworker.models import ProjectScan, VerificationResult


def verify_project(scan: ProjectScan) -> VerificationResult:
    checks = {
        "readme_found": scan.readme_found,
        "license_found": scan.license_found,
        "tests_found": scan.tests_found,
        "package_file_found": bool(scan.package_files),
        "entrypoint_found": bool(scan.entrypoints),
    }
    warnings: list[str] = []
    next_actions: list[str] = []

    if not checks["readme_found"]:
        warnings.append("No README detected.")
        next_actions.append("Add README.md with problem, solution, install, usage, and limitations.")
    if not checks["license_found"]:
        warnings.append("No LICENSE detected.")
        next_actions.append("Add a license or private-use notice.")
    if not checks["tests_found"]:
        warnings.append("No tests detected.")
        next_actions.append("Add tests for scanner, scoring, verification, and CLI.")
    if not checks["package_file_found"]:
        warnings.append("No package/dependency file detected.")
        next_actions.append("Add pyproject.toml, package.json, or requirements.txt.")
    if not checks["entrypoint_found"]:
        warnings.append("No obvious app/CLI entrypoint detected.")
        next_actions.append("Add cli.py, app.py, main.py, or documented run command.")

    passed = all(checks.values())
    return VerificationResult(passed=passed, checks=checks, warnings=warnings, next_actions=next_actions)
