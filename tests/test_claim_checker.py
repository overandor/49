from overworker.verification.claim_checker import ClaimLabel, label_claim


def test_labels_speculative_claims():
    claim = label_claim('This has guaranteed funding and $1.2M value')
    assert claim.label == ClaimLabel.SPECULATIVE


def test_labels_evidence_like_claims_as_inferred():
    claim = label_claim('The repo has a demo and benchmark logs')
    assert claim.label == ClaimLabel.INFERRED
