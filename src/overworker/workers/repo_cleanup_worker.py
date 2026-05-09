from overworker.workers.code_worker import code_cleanup_tasks


def repo_cleanup_plan(files: list[str]) -> str:
    tasks = code_cleanup_tasks(files)
    if not tasks:
        return "# Repo Cleanup Plan\n\nNo critical packaging gaps detected."
    return "# Repo Cleanup Plan\n\n" + "\n".join(f"- {task}" for task in tasks)
