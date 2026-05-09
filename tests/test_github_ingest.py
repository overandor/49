from overworker.github_ingest import is_supported_text_file, parse_github_url


def test_parse_github_url_https():
    owner, repo = parse_github_url('https://github.com/overandor/49')
    assert owner == 'overandor'
    assert repo == '49'


def test_parse_github_url_git_suffix():
    owner, repo = parse_github_url('git@github.com:overandor/49.git')
    assert owner == 'overandor'
    assert repo == '49'


def test_supported_text_file():
    assert is_supported_text_file('README.md')
    assert is_supported_text_file('src/app.py')
    assert not is_supported_text_file('image.png')
