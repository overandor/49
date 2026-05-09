# GitHub Ingestion Spec

## Goal

Enable Overworker to scan a public GitHub repo URL and produce a verified deliverable package.

## MVP behavior

Input:

```text
https://github.com/{owner}/{repo}
```

Output:

```text
scan.json
verification-report.json
overwork-score.json
secret-findings.json
claim-labels.json
sample-report.md
overworker-package.zip
```

## Required steps

1. Parse repo URL.
2. Fetch repository metadata.
3. Fetch file tree.
4. Download supported text files under size limits.
5. Identify README, license, package files, tests, entrypoints, docs, deployment files.
6. Run Verification Firewall.
7. Run Secret Scanner.
8. Label claims in README/docs.
9. Compute Overwork Score.
10. Export report bundle.

## Safety boundaries

- Do not execute repo code by default.
- Do not run shell commands unless explicitly enabled.
- Do not send private repo contents to external LLMs without consent.
- Redact detected secrets from reports.
- Label claims as verified, inferred, user-provided, unsupported, or speculative.

## Future implementation options

### Public no-token mode

Use GitHub public raw/tree endpoints with rate limits.

### Token mode

Use `GITHUB_TOKEN` for higher limits and private repos with explicit user permission.

## Acceptance criteria

A user can paste a public GitHub URL and receive a package in under 5 minutes for repos under 10 MB of text files.
