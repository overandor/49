from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from overworker.chat_archive_parser import parse_chat_archive
from overworker.llm import remote_no_key_reply
from overworker.repo_scanner import scan_repo
from overworker.scoring.overwork_score import score_project
from overworker.verification.firewall import verify_project
from overworker.export.markdown_exporter import render_report

APP_DIR = Path(__file__).parent

app = FastAPI(title="Overworker Dashboard", version="0.2.0")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "service": "overworker-dashboard"}


@app.post("/api/analyze-text")
async def analyze_text(text: str = Form(...)) -> JSONResponse:
    signals = parse_chat_archive(text)
    llm = await remote_no_key_reply(
        "Analyze this Overworker archive input. Return product thesis, risks, and next actions.\n\n" + text
    )
    return JSONResponse(
        {
            "signals": {
                "product_names": signals.product_names,
                "risk_terms": signals.risk_terms,
                "action_terms": signals.action_terms,
            },
            "llm": {
                "provider": llm.provider,
                "ok": llm.ok,
                "error": llm.error,
                "text": llm.text,
            },
        }
    )


@app.post("/api/demo-report")
async def demo_report() -> JSONResponse:
    root = Path.cwd()
    scan = scan_repo(root)
    verification = verify_project(scan)
    score = score_project(scan, verification)
    report = render_report(scan, verification, score)
    return JSONResponse(
        {
            "scan": scan.to_dict(),
            "verification": verification.to_dict(),
            "score": score.to_dict(),
            "report_markdown": report,
        }
    )


@app.post("/api/mock-upload-report")
async def mock_upload_report(project_name: str = Form("Sample Project"), readme: str = Form("")) -> JSONResponse:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        if readme.strip():
            (root / "README.md").write_text(readme)
        (root / "pyproject.toml").write_text("[project]\nname='sample'\n")
        (root / "src").mkdir()
        (root / "src" / "cli.py").write_text("print('hello')\n")
        scan = scan_repo(root)
        verification = verify_project(scan)
        score = score_project(scan, verification)
        report = render_report(scan, verification, score)
        return JSONResponse(
            {
                "project_name": project_name,
                "scan": scan.to_dict(),
                "verification": verification.to_dict(),
                "score": score.to_dict(),
                "report_markdown": report,
            }
        )
