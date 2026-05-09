from __future__ import annotations

from overworker.models import OverworkScore, ProjectScan, VerificationResult


def score_project(scan: ProjectScan, verification: VerificationResult | None = None) -> OverworkScore:
    concept_clarity = 0.60 if scan.readme_found else 0.25
    implementation_evidence = min(1.0, 0.20 + len(scan.entrypoints) * 0.20 + len(scan.package_files) * 0.10)
    documentation_quality = 0.65 if scan.readme_found else 0.20
    demo_readiness = 0.55 if scan.entrypoints else 0.20
    verification_strength = 0.55 if scan.tests_found else 0.20
    commercial_packaging = 0.60 if scan.license_found and scan.readme_found else 0.25

    if verification:
        verification_strength = max(verification_strength, 0.70 if verification.passed else 0.30)

    return OverworkScore(
        concept_clarity=round(concept_clarity, 4),
        implementation_evidence=round(implementation_evidence, 4),
        documentation_quality=round(documentation_quality, 4),
        demo_readiness=round(demo_readiness, 4),
        verification_strength=round(verification_strength, 4),
        commercial_packaging=round(commercial_packaging, 4),
    )
