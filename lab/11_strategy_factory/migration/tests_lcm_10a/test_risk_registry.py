from .conftest import j,jl
def test_risk_assumptions_are_not_normalized():
 rows=jl('risk/risk_assumption_registry.jsonl');assert len(rows)==488;assert all(x['normalization_status']=='NOT_NORMALIZED' and not x['behavior_change_performed'] for x in rows)
