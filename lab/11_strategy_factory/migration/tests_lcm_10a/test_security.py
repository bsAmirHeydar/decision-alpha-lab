from .conftest import j,jl
def test_security_records_default_disabled():
 rows=jl('security/security_restricted_execution_paths.jsonl');assert len(rows)==818;assert all(x['restriction_state']=='SECURITY_REVIEW_REQUIRED' and not x['adapter_activation_allowed'] and not x['live_order_authority'] for x in rows)
