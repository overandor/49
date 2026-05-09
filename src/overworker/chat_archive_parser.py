from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class ArchiveSignals:
    product_names: list[str]
    risk_terms: list[str]
    action_terms: list[str]


def parse_chat_archive(text: str) -> ArchiveSignals:
    products = sorted(set(re.findall(r"\b(Overworker|AlphaSignalLLM|Bearinglessfull|Execution Firewall|Semantic Protocol Runtime|Couchify|Language\.fi)\b", text)))
    risk_terms = sorted(set(re.findall(r"\b(risk|disclaimer|compliance|valuation|tax|funding|investor|proof)\b", text, flags=re.I)))
    action_terms = sorted(set(re.findall(r"\b(build|ship|verify|score|export|audit|package|demo)\b", text, flags=re.I)))
    return ArchiveSignals(products, risk_terms, action_terms)
