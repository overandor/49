from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from overworker.chat_archive_parser import parse_chat_archive
from overworker.export.markdown_exporter import render_report, write_report
from overworker.export.zip_exporter import export_zip
from overworker.llm import remote_no_key_reply
from overworker.repo_scanner import scan_repo
from overworker.scoring.overwork_score import score_project
from overworker.verification.claim_checker import label_claims
from overworker.verification.firewall import verify_project
from overworker.verification.secret_scanner import scan_path_for_secrets, scan_text_for_secrets

APP_DIR = Path(__file__).parent

app = FastAPI(title="Overworker Dashboard", version="0.3.0")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def build_report_payload(root: Path) -> dict:
    scan = scan_repo(root)
    verification = verify_project(scan)
    score = score_project(scan, verification)
    report = render_report(scan, verification, score)
    secrets = scan_path_for_secrets(root)
    return {
        "scan": scan.to_dict(),
        "verification": verification.to_dict(),
        "score": score.to_dict(),
        "secrets": secrets,
        "report_markdown": report,
    }


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "service": "overworker-dashboard", "version": "0.3.0"}


@app.post("/api/analyze-text")
async def analyze_text(text: str = Form(...)) -> JSONResponse:
    signals = parse_chat_archive(text)
    claims = [line.strip("-• ") for line in text.splitlines() if line.strip()][:20]
    labeled = label_claims(claims)
    secret_findings = [f.to_dict() for f in scan_text_for_secrets(text, "archive-input")]
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
            "claims": labeled,
            "secrets": secret_findings,
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
    return JSONResponse(build_report_payload(Path.cwd()))


@app.post("/api/mock-upload-report")
async def mock_upload_report(project_name: str = Form("Sample Project"), readme: str = Form("")) -> JSONResponse:
    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        if readme.strip():
            (root / "README.md").write_text(readme)
        (root / "pyproject.toml").write_text("[project]\nname='sample'\n")
        (root / "src").mkdir()
        (root / "src" / "cli.py").write_text("print('hello')\n")
        payload = build_report_payload(root)
        payload["project_name"] = project_name
        return JSONResponse(payload)


@app.post("/api/export-demo-package")
async def export_demo_package() -> JSONResponse:
    """Create a local demo report bundle and return the package path.

    In a production deployment this endpoint should return FileResponse after access control.
    """
    out = Path("out/dashboard-package")
    out.mkdir(parents=True, exist_ok=True)
    payload = build_report_payload(Path.cwd())
    (out / "scan.json").write_text(json.dumps(payload["scan"], indent=2))
    (out / "verification-report.json").write_text(json.dumps(payload["verification"], indent=2))
    (out / "overwork-score.json").write_text(json.dumps(payload["score"], indent=2))
    (out / "secret-findings.json").write_text(json.dumps(payload["secrets"], indent=2))
    write_report(out / "sample-report.md", payload["report_markdown"])
    zip_path = export_zip(out, "out/overworker-demo-package.zip")
    return JSONResponse({"ok": True, "package_path": str(zip_path), "files": [p.name for p in out.iterdir() if p.is_file()]})
