# Dashboard Runbook

## Purpose

The Overworker dashboard is a demo surface for the production-sale scaffold. It shows:

- Overwork Score
- Verification Firewall checks
- generated Markdown report
- archive signal extraction
- best-effort remote no-key LLM analysis with deterministic fallback

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
```

## Run dashboard

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open:

```text
http://localhost:8000
```

## API endpoints

```text
GET  /health
POST /api/demo-report
POST /api/mock-upload-report
POST /api/analyze-text
```

## LLM behavior

The dashboard uses `src/overworker/llm.py`.

Default behavior:

```text
Try public remote no-key text endpoint
→ if unavailable/throttled/errors
→ deterministic fallback
```

Environment controls:

```bash
OVERWORKER_DISABLE_REMOTE_LLM=true
OVERWORKER_PUBLIC_LLM_URL=https://text.pollinations.ai
OVERWORKER_PUBLIC_LLM_MODEL=openai
```

## Production caveat

Public no-key LLM endpoints are not reliability guarantees. They can throttle, change, fail, or require keys later. Production versions should support explicit provider credentials, local models, or enterprise-approved inference.

## Demo path

1. Click “Generate demo report.”
2. Review Overwork Score.
3. Review verification warnings.
4. Paste an archive note into LLM analyst.
5. Confirm either public remote or deterministic fallback returns an analysis.
