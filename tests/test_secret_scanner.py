from overworker.verification.secret_scanner import scan_text_for_secrets


def test_detects_generic_api_key():
    findings = scan_text_for_secrets('API_KEY=abcdefghijklmnop1234567890', 'x.env')
    assert findings
    assert findings[0].kind == 'generic_api_key'


def test_ignores_plain_text():
    assert scan_text_for_secrets('hello world') == []
