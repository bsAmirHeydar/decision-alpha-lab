from .conftest import jl,j
def test_parity_is_non_compensatory_and_has_no_hidden_failures():
 rows=jl("parity/setup_parity_registry.jsonl");assert len(rows)==60;assert all(x["aggregate_success_cannot_override"] for x in rows);assert all(x["parity_status"]=="BLOCKED" for x in rows);assert sum(x["hard_mismatch_count"] for x in rows)==0
def test_variance_registry_does_not_waive_mismatch():
 d=j("parity/setup_variance_decisions.json");assert d["hard_mismatch_count"]==0 and d["decisions"]==[]
