from __future__ import annotations

import hashlib
import os
import urllib.parse
from dataclasses import dataclass

import httpx


@dataclass
class LLMResult:
    text: str
    provider: str
    ok: bool
    error: str | None = None


def deterministic_reply(prompt: str) -> LLMResult:
    digest = hashlib.sha256(prompt.encode()).hexdigest()[:8]
    text = (
        "Overworker deterministic analyst fallback\n\n"
        "Summary: This project should be evaluated by evidence, not narrative. "
        "Package the repo, verify files, label unsupported claims, and export a report.\n\n"
        f"Trace: {digest}"
    )
    return LLMResult(text=text, provider="deterministic_fallback", ok=True)


async def remote_no_key_reply(prompt: str, timeout_seconds: float = 12.0) -> LLMResult:
    """Best-effort no-key remote LLM call.

    This uses a public text-generation endpoint when available and falls back deterministically.
    Public no-key endpoints can throttle, change, or fail. This is suitable for demos, not
    production guarantees.
    """
    if os.getenv("OVERWORKER_DISABLE_REMOTE_LLM", "false").lower() == "true":
        return deterministic_reply(prompt)

    base = os.getenv("OVERWORKER_PUBLIC_LLM_URL", "https://text.pollinations.ai")
    model = os.getenv("OVERWORKER_PUBLIC_LLM_MODEL", "openai")
    safe_prompt = (
        "You are Overworker, a sober technical due-diligence analyst. "
        "Return concise, evidence-based output. Do not guarantee funding.\n\n"
        + prompt[:4000]
    )
    url = f"{base}/{urllib.parse.quote(safe_prompt)}?model={urllib.parse.quote(model)}"

    try:
        async with httpx.AsyncClient(timeout=timeout_seconds, follow_redirects=True) as client:
            resp = await client.get(url)
            if resp.status_code >= 400:
                fallback = deterministic_reply(prompt)
                fallback.error = f"public_llm_http_{resp.status_code}"
                return fallback
            text = resp.text.strip()
            if not text:
                fallback = deterministic_reply(prompt)
                fallback.error = "empty_public_llm_response"
                return fallback
            return LLMResult(text=text[:4000], provider="public_no_key_remote", ok=True)
    except Exception as exc:  # noqa: BLE001
        fallback = deterministic_reply(prompt)
        fallback.error = str(exc)
        return fallback
