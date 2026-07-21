from .conftest import j,jl
def test_all_authority_dimensions_false():
 rows=jl('authority/authority_boundary_map.jsonl');assert len(rows)==1190
 for x in rows:
  for k in ('request_intent_authority','submission_authority','modify_authority','cancel_authority','reconcile_authority','close_authority','runtime_authority','live_order_authority','capital_authority'):assert x[k] is False
