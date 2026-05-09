from overworker.models import ProjectScan
from overworker.scoring.overwork_score import score_project


def test_score_uses_weakest_link():
    scan = ProjectScan(
        root='.',
        files=['README.md', 'pyproject.toml', 'LICENSE', 'src/overworker/cli.py'],
        readme_found=True,
        tests_found=False,
        license_found=True,
        package_files=['pyproject.toml'],
        entrypoints=['src/overworker/cli.py'],
    )
    score = score_project(scan)
    assert score.final_score() == min(
        score.concept_clarity,
        score.implementation_evidence,
        score.documentation_quality,
        score.demo_readiness,
        score.verification_strength,
        score.commercial_packaging,
    )
    assert score.weakest_component() == 'verification_strength'
