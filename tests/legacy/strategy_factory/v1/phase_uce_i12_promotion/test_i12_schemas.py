import json
from pathlib import Path
import jsonschema
ROOT=Path(__file__).resolve().parents[2]
SCHEMA_DIR=ROOT/'schemas'/'v3'
NAMES=(
'promotion_trial_evidence','promotion_selection_universe','promotion_family_definition','promotion_test_evidence',
'promotion_uncertainty_request','promotion_uncertainty_report','promotion_sequential_confidence_report',
'promotion_multiplicity_report','promotion_nested_selection_audit','promotion_universe_reconciliation',
'promotion_pbo_report','promotion_deflated_performance_report','promotion_reality_check_report','promotion_spa_report',
'promotion_null_control_plan','promotion_null_control_result','promotion_stress_plan','promotion_stress_result',
'promotion_calibration_report','promotion_prospective_challenge_freeze','promotion_policy','promotion_model_risk_scorecard',
'promotion_evidence_bundle','promotion_decision','promotion_registry_snapshot')

def load(name): return json.loads((SCHEMA_DIR/f'{name}.schema.json').read_text())
def test_exact_schema_count_and_presence(): assert len(NAMES)==25 and all((SCHEMA_DIR/f'{n}.schema.json').is_file() for n in NAMES)
def test_all_schemas_are_closed_draft_2020_12():
    for n in NAMES:
        s=load(n); assert s['$schema']=='https://json-schema.org/draft/2020-12/schema'; assert s['type']=='object'; assert s['additionalProperties'] is False
def test_all_schema_ids_match_file_names():
    for n in NAMES: assert load(n)['$id'].endswith(f'/{n}.schema.json')
def test_selection_universe_example_validates():
    schema=load('promotion_selection_universe'); schema['properties']['trials']['items']=load('promotion_trial_evidence'); data=json.loads((ROOT/'examples'/'uce_i12'/'selection_universe_golden.json').read_text()); jsonschema.validate(data,schema)
def test_policy_example_validates(): jsonschema.validate(json.loads((ROOT/'examples'/'uce_i12'/'promotion_policy_golden.json').read_text()),load('promotion_policy'))
def test_multiplicity_example_validates(): jsonschema.validate(json.loads((ROOT/'examples'/'uce_i12'/'multiplicity_report_golden.json').read_text()),load('promotion_multiplicity_report'))
def test_registry_example_validates(): jsonschema.validate(json.loads((ROOT/'examples'/'uce_i12'/'promotion_registry_snapshot.json').read_text()),load('promotion_registry_snapshot'))
def test_schema_rejects_unknown_property():
    data=json.loads((ROOT/'examples'/'uce_i12'/'promotion_policy_golden.json').read_text()); data['unknown']=1
    try: jsonschema.validate(data,load('promotion_policy'))
    except jsonschema.ValidationError: pass
    else: raise AssertionError('unknown property accepted')
