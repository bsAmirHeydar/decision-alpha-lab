from .conftest import j,jl
def test_lcm01_order_and_network_misses_are_explicit_unknown():
 rows=jl('reconciliation/lcm01_capability_reconciliation.jsonl');unknowns=jl('unknowns/execution_unknown_queue.jsonl');subjects={x['subject_id'] for x in unknowns};assert rows
 for r in rows:
  if not r['lcm10a_deep_match'] and r['lcm01_capability_kind'] in {'ORDER_API','NETWORK_API'}:assert r['reconciliation_id'] in subjects
