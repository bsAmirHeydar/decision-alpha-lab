from tools.repository_paths import find_repository_root
import json
from pathlib import Path
import pytest,yaml
from jsonschema import Draft202012Validator
from saed_v4_constitution.contracts import load_document,validate_closed
from saed_v4_constitution.errors import ContractError

ROOT=find_repository_root(__file__); S=ROOT/'schemas/legacy/strategy_factory/saed_v4_00'; E=ROOT/'examples/legacy/strategy_factory/saed_v4_00'

@pytest.mark.parametrize('name,doc',[
 ('research_constitution','research_constitution.yaml'),('authority_matrix','authority_matrix.yaml'),('evidence_role_policy','evidence_role_policy.yaml'),('objective_policy','objective_policy.yaml'),('baseline_policy','baseline_policy.yaml'),('program_manifest','program_manifest.json'),('crosswalk','ucee_i01_i18_crosswalk.json'),('exposure_budget','exposure_budget.json'),('external_evidence_claim','external_static_evidence_claim.json'),('handoff','phase_handoff_v4_00_to_v4_01.json')])
def test_examples_validate(name,doc):
 schema=json.loads((S/f'{name}.schema.json').read_text()); validate_closed(load_document(E/doc),schema)

def test_unknown_field_rejected():
 schema=json.loads((S/'program_manifest.schema.json').read_text()); doc=json.loads((E/'negative/program_manifest_unknown_field.json').read_text())
 with pytest.raises(ContractError): validate_closed(doc,schema)

def test_order_authority_const_rejected():
 schema=json.loads((S/'research_constitution.schema.json').read_text()); doc=yaml.safe_load((E/'negative/constitution_with_order_authority.yaml').read_text())
 with pytest.raises(ContractError): validate_closed(doc,schema)

@pytest.mark.parametrize('path',sorted(S.glob('*.schema.json')))
def test_all_schemas_are_draft_2020_closed(path):
 s=json.loads(path.read_text()); Draft202012Validator.check_schema(s); assert s.get('additionalProperties') is False
