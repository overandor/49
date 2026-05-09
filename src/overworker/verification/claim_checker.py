from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum


class ClaimLabel(str, Enum):
    VERIFIED = "verified"
    INFERRED = "inferred"
    USER_PROVIDED = "user_provided"
    UNSUPPORTED = "unsupported"
    SPECULATIVE = "speculative"


@dataclass
class LabeledClaim:
    text: str
    label: ClaimLabel
    reason: str

    def to_dict(self) -> dict:
        data = asdict(self)
        data["label"] = self.label.value
        return data


SPECULATIVE_TERMS = [
    "guaranteed funding",
    "guaranteed investor",
    "$1.2m",
    "$200,000+",
    "patentable",
    "tax credit guaranteed",
    "risk free",
    "guaranteed profit",
]

EVIDENCE_TERMS = ["repo", "demo", "test", "log", "screenshot", "benchmark", "customer", "pilot"]


def label_claim(text: str) -> LabeledClaim:
    low = text.lower()
    if any(term in low for term in SPECULATIVE_TERMS):
        return LabeledClaim(text, ClaimLabel.SPECULATIVE, "Contains valuation, funding, legal, tax, or profit language requiring evidence and disclaimers.")
    if any(term in low for term in EVIDENCE_TERMS):
        return LabeledClaim(text, ClaimLabel.INFERRED, "Mentions evidence-like artifacts but still requires source verification.")
    if low.startswith("user says") or low.startswith("founder claims"):
        return LabeledClaim(text, ClaimLabel.USER_PROVIDED, "Statement is user-provided and not independently verified.")
    return LabeledClaim(text, ClaimLabel.UNSUPPORTED, "No explicit evidence marker detected.")


def label_claims(claims: list[str]) -> list[dict]:
    return [label_claim(c).to_dict() for c in claims if c.strip()]
