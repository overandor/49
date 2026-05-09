# Hugging Face Space Deployment

## Space type

Use Docker or Python/Gradio-compatible runtime with FastAPI served by uvicorn.

## Start command

```bash
uvicorn app:app --host 0.0.0.0 --port 7860
```

## Required files

```text
app.py
requirements.txt
app/main.py
app/templates/index.html
app/static/style.css
app/static/app.js
src/overworker/
```

## Environment variables

```text
OVERWORKER_ENV=production
OVERWORKER_DISABLE_REMOTE_LLM=false
OVERWORKER_PUBLIC_LLM_URL=https://text.pollinations.ai
OVERWORKER_PUBLIC_LLM_MODEL=openai
```

## Caveat

The remote no-key LLM is best-effort. The dashboard remains functional through deterministic fallback if the public endpoint fails.
