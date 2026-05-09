#!/usr/bin/env python3
from overworker.repo_scanner import scan_repo
from overworker.verification.firewall import verify_project
from overworker.scoring.overwork_score import score_project
import json
import sys

path = sys.argv[1] if len(sys.argv) > 1 else '.'
scan = scan_repo(path)
verification = verify_project(scan)
score = score_project(scan, verification)
print(json.dumps(score.to_dict(), indent=2))
