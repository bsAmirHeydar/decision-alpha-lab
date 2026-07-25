import json
from tools.strategy_factory.lcm.lcm_10b.schema_validation import validate_instance
from .conftest import ROOT,SCHEMAS,j,jl
def test_representative_instances_validate():
 r=jl("registries/treatment_package_registry.jsonl")[0];validate_instance(SCHEMAS,"treatment_package_registry_record",r);validate_instance(SCHEMAS,"treatment_package",json.loads((ROOT/r["package_path"]).read_text()));validate_instance(SCHEMAS,"execution_adapter_contract",j(f"execution_adapter_contracts/{jl('execution_adapter_contracts/execution_adapter_contract_registry.jsonl')[0]['adapter_id']}.json"));validate_instance(SCHEMAS,"blocker_record",jl("blockers/treatment_blocker_registry.jsonl")[0]);validate_instance(SCHEMAS,"setup_binding_record",jl("bindings/setup_treatment_package_binding_registry.jsonl")[0]);validate_instance(SCHEMAS,"handoff",j("handoff/lcm10b_to_lcm10c_handoff.json"))
