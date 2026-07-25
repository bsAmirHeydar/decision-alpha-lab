import json
from pathlib import Path
import jsonschema
import pytest
ROOT=Path(__file__).resolve().parents[2];D=ROOT/'schemas'/'v3'
NAMES=('policy_promotion_admission','policy_predicate','policy_exception_rule','policy_manual_definition','policy_context_occurrence','policy_manual_decision','policy_model_output','policy_fallback_rule','policy_fallback_policy','policy_authority_rule','policy_authority_matrix','policy_operator_override','policy_node_spec','policy_graph_spec','policy_compiled_graph','policy_node_trace','policy_decision','policy_attribution_opportunity','policy_incremental_value_report','policy_replay_manifest','policy_conflict_event','policy_abstention_event','policy_capability_manifest','policy_registry_snapshot','policy_handoff_bundle')
def load(n):return json.loads((D/f'{n}.schema.json').read_text())
def test_schema_count():assert len(NAMES)==25 and all((D/f'{n}.schema.json').is_file() for n in NAMES)
def test_schemas_closed():
    for n in NAMES:
        s=load(n);assert s['$schema']=='https://json-schema.org/draft/2020-12/schema' and s['additionalProperties'] is False
def test_ids_match_names():
    for n in NAMES:assert load(n)['$id'].endswith(f'/{n}.schema.json')
def test_admission_example_valid():jsonschema.validate(json.loads((ROOT/'examples/uce_i13/promotion_admission_golden.json').read_text()),load('policy_promotion_admission'))
def test_manual_example_valid():jsonschema.validate(json.loads((ROOT/'examples/uce_i13/manual_policy_golden.json').read_text()),load('policy_manual_definition'))
def test_output_example_valid():jsonschema.validate(json.loads((ROOT/'examples/uce_i13/model_output_golden.json').read_text()),load('policy_model_output'))
def test_graph_example_valid():jsonschema.validate(json.loads((ROOT/'examples/uce_i13/hybrid_graph_golden.json').read_text()),load('policy_graph_spec'))
def test_registry_example_valid():jsonschema.validate(json.loads((ROOT/'examples/uce_i13/policy_registry_snapshot.json').read_text()),load('policy_registry_snapshot'))
def test_unknown_property_rejected():
    d=json.loads((ROOT/'examples/uce_i13/promotion_admission_golden.json').read_text());d['x']=1
    with pytest.raises(jsonschema.ValidationError):jsonschema.validate(d,load('policy_promotion_admission'))
