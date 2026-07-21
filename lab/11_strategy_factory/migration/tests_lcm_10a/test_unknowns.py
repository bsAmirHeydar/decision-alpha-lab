from .conftest import j,jl
def test_unknown_queue_is_first_class_and_unique():
 rows=jl('unknowns/execution_unknown_queue.jsonl');assert len(rows)==4302;assert len({x['unknown_id'] for x in rows})==len(rows);assert all(x['resolution_state']=='OPEN' for x in rows)
