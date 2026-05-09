def code_cleanup_tasks(files: list[str]) -> list[str]:
    tasks = []
    if not any(f.endswith('README.md') or f.endswith('readme.md') for f in files):
        tasks.append('Add README.md')
    if not any('test' in f.lower() for f in files):
        tasks.append('Add tests')
    if not any(f in {'pyproject.toml','package.json','requirements.txt'} for f in files):
        tasks.append('Add dependency/package file')
    return tasks
