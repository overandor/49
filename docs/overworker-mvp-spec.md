# Overworker MVP Spec

## MVP name

**Overworker for GitHub R&D Cleanup**

## MVP promise

Upload or connect a messy technical project. Overworker returns a structured package that explains what exists, what works, what is missing, and what must be done next.

## MVP input

Minimum supported inputs:

```text
GitHub repo URL or uploaded ZIP
README or missing README
file tree
package files
source files
optional chat archive
optional Hugging Face Space links
```

## MVP output

The MVP should generate:

```text
1. repo-map.md
2. product-thesis.md
3. technical-asset-map.md
4. README-draft.md
5. demo-plan.md
6. risk-disclosure.md
7. issue-roadmap.md
8. overwork-score.json
9. verification-report.md
```

## Core user story

As a technical founder with scattered project assets, I want Overworker to inspect my project and generate a credible, structured product package so that investors, users, collaborators, or reviewers can understand the work quickly.

## Non-goals for MVP

Do not build:

```text
autonomous live trading
a full general AI agent
fundraising automation
legal/tax guarantees
complex multi-user workspace
marketplace operations
voice interface
hardware loop
```

## Required features

### 1. Project ingestion

- Accept a repo URL or uploaded ZIP.
- Extract file tree.
- Identify package files.
- Identify README, docs, examples, tests, config, deployment files.

### 2. Asset extraction

Detect:

```text
product names
entry points
APIs
scripts
models
datasets
notebooks
deployment files
documentation
missing files
```

### 3. Claim labeling

Every claim should be labeled:

```text
verified
inferred
user-provided
unsupported
speculative
```

### 4. Overwork Score

Compute weakest-link readiness score:

```text
Concept Clarity
Implementation Evidence
Documentation Quality
Demo Readiness
Verification Strength
Commercial Packaging
```

### 5. Verification report

Check:

```text
README exists
install instructions exist
tests exist
entrypoint exists
demo exists
license exists
dependencies listed
secrets absent
unsupported claims flagged
```

### 6. Deliverable export

Export Markdown + JSON bundle.

## Example CLI

```bash
overworker scan https://github.com/overandor/48 --out ./overworker-report
overworker score ./overworker-report
overworker export ./overworker-report --zip
```

## Example web flow

```text
Paste repo URL
→ Scan project
→ Review detected assets
→ Generate package
→ Verify claims
→ Export ZIP
```

## Success metrics

The MVP succeeds if:

```text
A repo can be scanned in under 5 minutes.
The output package has at least 8 generated files.
A user can understand the project in under 2 minutes.
The report identifies at least 5 concrete next actions.
Unsupported claims are visibly labeled.
```

## 30-day build target

By day 30, Overworker should process one repo and one chat archive into a usable package.

## 90-day build target

By day 90, Overworker should support multiple repos, public demo, sample reports, Overwork Score, and 3 pilot users.
