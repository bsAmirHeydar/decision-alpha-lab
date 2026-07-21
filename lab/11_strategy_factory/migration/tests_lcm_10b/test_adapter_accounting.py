from .conftest import jl
def test_every_execution_source_has_disabled_adapter():
 rows=jl("execution_adapter_contracts/execution_adapter_contract_registry.jsonl");assert len(rows)==483;assert len({x["source_path"] for x in rows})==483;assert all(not x["submission_capability_default"] and not x["live_mode_allowed"] and not x["paper_mode_allowed"] for x in rows)
