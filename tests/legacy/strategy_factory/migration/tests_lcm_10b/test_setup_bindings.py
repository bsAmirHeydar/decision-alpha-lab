from .conftest import jl
def test_all_setups_are_package_or_blocker():
 rows=jl("bindings/setup_treatment_package_binding_registry.jsonl");assert len(rows)==60;assert len({x["setup_id"] for x in rows})==60;assert all(bool(x["treatment_package_ids"])!=bool(x["blocker_ids"]) for x in rows);assert all(not x["execution_authorized"] for x in rows)
