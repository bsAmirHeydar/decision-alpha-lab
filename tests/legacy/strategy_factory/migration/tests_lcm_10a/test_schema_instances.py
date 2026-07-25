import json
from jsonschema import Draft202012Validator
from .conftest import SCHEMAS,j,jl
def val(name,doc):
 s=json.loads((SCHEMAS/f'{name}.schema.json').read_text());e=list(Draft202012Validator(s).iter_errors(doc));assert not e,[x.message for x in e[:5]]
def test_representative_instances_match_schemas():
 val('source_file_record',jl('source/source_file_freeze.jsonl')[0]);val('treatment_atom_record',jl('inventory/treatment_atom_registry.jsonl')[0]);val('execution_capability_record',jl('execution/execution_capability_registry.jsonl')[0]);val('reachability_record',jl('reachability/broker_api_reachability.jsonl')[0]);val('authority_boundary_record',jl('authority/authority_boundary_map.jsonl')[0]);val('risk_assumption_record',jl('risk/risk_assumption_registry.jsonl')[0]);val('execution_unknown_record',jl('unknowns/execution_unknown_queue.jsonl')[0]);val('setup_treatment_binding_record',jl('bindings/setup_treatment_binding_inventory.jsonl')[0]);val('security_record',jl('security/security_restricted_execution_paths.jsonl')[0]);val('handoff',j('handoff/lcm10a_to_lcm10b_handoff.json'));val('receipt',j('treatment_inventory_receipt.json'));val('marker',j('treatment_inventory_marker.json'));val('required_artifact_locator',j('required_artifact_locator.json'));val('extraction_plan',j('plans/treatment_extraction_order.json'))
