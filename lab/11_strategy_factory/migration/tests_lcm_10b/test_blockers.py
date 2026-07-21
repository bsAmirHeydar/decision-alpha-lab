from .conftest import jl
def test_blockers_are_explicit_and_open():
 rows=jl("blockers/treatment_blocker_registry.jsonl");assert len(rows)==382;assert all(x["blocking"] and x["resolution_state"]=="OPEN" and x["blocker_codes"] for x in rows)
