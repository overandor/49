from overworker.worker_router import route_worker


def test_routes_investor_tasks():
    assert route_worker('make investor one-pager') == 'investor_worker'


def test_routes_docs_tasks():
    assert route_worker('write README docs') == 'docs_worker'
