# Overworker / Operator Workflow Vault

> Research-grade scaffold for converting fragmented technical work into verified deliverable packages.

Overworker is an early-stage AI work-execution system for founders, operators, and technical teams with scattered repos, chats, demos, product ideas, and R&D artifacts. The project treats LLM sessions, code fragments, dashboards, simulations, notes, and provenance records as compounding operator-intelligence assets — while explicitly separating narrative from defensible technical proof.

## Core thesis

AI-native builders increasingly generate more project material than they can consolidate. The bottleneck is no longer ideation. The bottleneck is completion, verification, provenance, and packaging.

Overworker investigates whether messy technical work can be transformed into structured deliverables through a repeatable pipeline:

```text
messy technical archive
→ project memory
→ repo/chat ingestion
→ worker routing
→ verification firewall
→ Overwork Score
→ investor/developer-ready package
```

The practical claim is modest: technical work becomes more commercially useful when it is made legible, inspectable, scored, and packaged.

## Current status

This is not yet a mature venture-scale product. It is a provenance archive plus production-sale scaffold.

```text
Conceptual narrative:        high
Prototype-stage IP:          meaningful
Defensible technical asset:  limited but improving
Production readiness:        early scaffold
Commercial readiness:        serviceable after packaging/proof
```

The repo now includes an installable Python package shape, CLI entry point, repository scanner, verification firewall, Overwork Score, report exporter, sales/proof docs, tests, and CI.

## Product definition

**Overworker is an AI work-execution and project-productization system that converts fragmented technical assets into verified deliverable packages.**

It is not positioned as a generic chatbot. The product boundary is:

```text
Input: messy project material
Output: structured deliverable package
Gate: verification report
Metric: Overwork Score
```

Initial wedge: **GitHub / R&D cleanup for AI builders and technical founders.**

## Architecture

```text
User / Operator Intent
        ↓
Project Memory
        ↓
Ingestion Layer
        ↓
Repo Scanner + Chat Archive Parser
        ↓
Worker Router
        ↓
Specialized Workers
        ↓
Verification Firewall
        ↓
Overwork Score
        ↓
Markdown / JSON / ZIP Export
```

## Main modules

| Module | Purpose |
|---|---|
| `repo_scanner.py` | Detects files, README, tests, package files, entrypoints, license |
| `chat_archive_parser.py` | Extracts product/risk/action signals from chat archives |
| `worker_router.py` | Routes tasks to docs, investor, IP, risk, repo cleanup, or research workers |
| `verification/firewall.py` | Checks whether a project has minimum package-readiness evidence |
| `scoring/overwork_score.py` | Computes weakest-link readiness score |
| `export/markdown_exporter.py` | Renders project reports |
| `cli.py` | Provides `overworker scan` and `overworker score` commands |

## Overwork Score

The Overwork Score is a weakest-link commercial-readiness score:

```text
Overwork Score = min(
  Concept Clarity,
  Implementation Evidence,
  Documentation Quality,
  Demo Readiness,
  Verification Strength,
  Commercial Packaging
)
```

| Score | State |
|---:|---|
| 0.00–0.20 | Idea Pile |
| 0.20–0.40 | Prototype Mess |
| 0.40–0.60 | R&D Asset |
| 0.60–0.80 | Demoable Product |
| 0.80–1.00 | Investor-Ready Package |

A technically interesting repo with no README, no demo, no tests, and unsupported claims remains hard to sell, fund, or evaluate.

## Verification Firewall

The Verification Firewall prevents narrative output from being treated as completed work.

Initial checks:

```text
README exists
license exists
tests exist
package/dependency file exists
entrypoint exists
```

Future checks:

```text
claim support labels
secret scanning
dependency validation
demo command execution
benchmark evidence
provenance links
risk disclosure completeness
```

Core principle: **work is not complete until it survives verification.**

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e . pytest
pytest -q
```

Run CLI:

```bash
overworker --help
overworker scan . --out out/report
overworker score .
```

Docker:

```bash
docker build -t overworker .
docker run --rm overworker
```

## Example output

`overworker scan . --out out/report` produces:

```text
out/report/scan.json
out/report/verification-report.json
out/report/overwork-score.json
out/report/sample-report.md
```

The report includes file count, README status, license status, test status, package-file detection, entrypoint detection, Overwork Score, weakest component, verification warnings, and next actions.

## Evidence standard

This repo separates three evidence tiers:

### Narrative

Names, theses, concepts, positioning, and metaphors. These are not defensible alone.

### Prototype-stage IP

Code, tests, package files, CLI commands, reports, dashboards, simulations, and provenance archives.

### Defensible technical asset

Requires working demo, repeatable outputs, telemetry/logs, tests, documentation, user or buyer proof, and clear disclaimers.

## Commercial form

Best first commercial offer: **Overworker Investor-Ready R&D Package Sprint**.

A fixed-scope service that turns messy technical work into:

- product thesis
- technical asset map
- README/docs plan
- demo checklist
- IP/moat summary
- risk disclosure
- use-of-funds plan
- pitch email
- investor FAQ
- 30/60/90 roadmap
- Overwork Score
- verification report

Suggested pricing:

```text
Audit only: $500–$1,500
Investor package sprint: $5,000
Full package + repo/demo cleanup: $10,000
Ongoing support: $2,500–$5,000/month
```

The service guarantees deliverables, not investor outcomes.

## Claims boundaries

This repository does not claim guaranteed investor interest, funding, valuation, tax credits, patentability, acquisition, trading profits, legal advice, or securities advice. All legal, tax, securities, investment, IP, and compliance claims require qualified professional review.

## Relationship to prior R&D assets

| Prior asset | Role inside Overworker |
|---|---|
| AlphaSignalLLM | Market analysis worker / proof of signal-memory workflows |
| Execution Firewall | Verification and clearance layer |
| Bearinglessfull Collateral | Weakest-link risk primitive inspiration |
| Semantic Protocol Runtime | Possible execution/policy runtime |
| Couchify / HandshakeOps | Marketplace workflow case study |
| Language.fi | Natural-language interface direction |
| Operator-Intelligence Assets | Provenance/archive layer |

## Roadmap

### Phase 1 — Scaffold and proof

CLI scanner, Overwork Score, verification report, sample outputs, tests, CI, and research-grade README.

### Phase 2 — Working MVP

Scan GitHub repo URL or uploaded ZIP, parse chat archive, generate deliverable package, export Markdown/JSON/ZIP, add claim labeling and secret scanner.

### Phase 3 — Sales-ready service

Sample client case study, before/after demo, pricing page, delivery checklist, proposal template, and first pilot.

### Phase 4 — SaaS platform

Web UI, accounts/projects, project memory, report history, export bundles, paid plans, and audit logs.

## Due-diligence summary

```text
Current value: provenance + prototype scaffold
Current weakness: limited external proof
Best wedge: GitHub/R&D cleanup
Best first buyer: technical founder with messy repos
Highest-risk distraction: live MEV/sniping claims
Most defensible primitive: verification-gated deliverable pipeline
```

Final framing:

> Overworker is not valuable because it has many names. It becomes valuable when it repeatedly turns messy technical work into verified, inspectable, commercially useful packages.
