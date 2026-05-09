from overworker.models import ProjectScan
from overworker.verification.firewall import verify_project


def test_verification_flags_missing_readme_and_tests():
    scan = ProjectScan(
        root='.',
        files=['pyproject.toml'],
        readme_found=False,
        tests_found=False,
        license_found=False,
        package_files=['pyproject.toml'],
        entrypoints=[],
    )
    result = verify_project(scan)
    assert not result.passed
    assert not result.checks['readme_found']
    assert any('README' in w for w in result.warnings)
