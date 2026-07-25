from .conftest import j,jl
def test_capabilities_have_false_authority():
 r=j('execution/execution_capability_registry.json');rows=jl('execution/execution_capability_registry.jsonl');assert r['record_count']==len(rows)==1334;assert all(not x['live_order_authorized'] and not x['runtime_authorized'] and not x['capital_authorized'] for x in rows)
