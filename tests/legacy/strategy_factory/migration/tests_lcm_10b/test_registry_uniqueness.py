from .conftest import jl
def test_ids_are_unique_across_primary_registries():
 sets=[("treatment_package_id",jl("registries/treatment_package_registry.jsonl")),("adapter_id",jl("execution_adapter_contracts/execution_adapter_contract_registry.jsonl")),("blocker_id",jl("blockers/treatment_blocker_registry.jsonl")),("binding_id",jl("bindings/setup_treatment_package_binding_registry.jsonl"))]
 for key,rows in sets:assert len({x[key] for x in rows})==len(rows)
