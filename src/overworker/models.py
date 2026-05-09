from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any


class ClaimStatus(str, Enum):
    VERIFIED = "verified"
    INFERRED = "inferred"
    USER_PROVIDED = "user_provided"
    UNSUPPORTED = "unsupported"
    SPECULATIVE = "speculative"


@dataclass
class ProjectScan:
    root: str
    files: list[str]
    readme_found: bool
    tests_found: bool
    license_found: bool
    package_files: list[str]
    entrypoints: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class VerificationResult:
    passed: bool
    checks: dict[str, bool]
    warnings: list[str]
    next_actions: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class OverworkScore:
    concept_clarity: float
    implementation_evidence: float
    documentation_quality: float
    demo_readiness: float
    verification_strength: float
    commercial_packaging: float

    def final_score(self) -> float:
        return min(asdict(self).values())

    def weakest_component(self) -> str:
        values = asdict(self)
        return min(values, key=values.get)

    def state(self) -> str:
        score = self.final_score()
        if score < 0.20:
            return "Idea Pile"
        if score < 0.40:
            return "Prototype Mess"
        if score < 0.60:
            return "R&D Asset"
        if score < 0.80:
            return "Demoable Product"
        return "Investor-Ready Package"

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["final_score"] = round(self.final_score(), 4)
        data["weakest_component"] = self.weakest_component()
        data["state"] = self.state()
        return data
