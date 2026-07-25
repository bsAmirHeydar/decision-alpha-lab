import json
from pathlib import Path
import yaml
from jsonschema import Draft202012Validator
from tools.strategy_factory.acl_os.acl_04.policies import SCHEMA_ROOT,POLICY_ROOT
from tools.strategy_factory.acl_os.acl_04.validate_acl_04 import validate
from tools.strategy_factory.acl_os.acl_04.cli import main


def test_all_schemas_are_valid_and_closed():
    schemas=list(SCHEMA_ROOT.glob('*.schema.json'))
    assert len(schemas)>=20
    for path in schemas:
        schema=json.loads(path.read_text());Draft202012Validator.check_schema(schema);assert schema['additionalProperties'] is False


def test_all_policies_parse():
    policies=list(POLICY_ROOT.glob('*.yaml'));assert len(policies)>=14
    for path in policies: assert isinstance(yaml.safe_load(path.read_text()),dict)


def test_static_validation_passes():
    result=validate();assert result['passed']
    assert result['claim_ceiling']=='SETUP_DEFINITION_REFERENCE_ONLY'


def test_cli_builds(fixtures,tmp_path,capsys):
    code=main([str(fixtures['acl03']),str(tmp_path/'out'),'--authority-permit',str(fixtures['root']/'authority_permit.json'),'--search-authority',str(fixtures['root']/'search_authority.json'),'--treatment-envelope',str(fixtures['root']/'treatment_envelope.json'),'--human-setup',str(fixtures['root']/'human_setup.yaml'),'--ai-request',str(fixtures['root']/'ai_request.json')])
    assert code==0
    payload=json.loads(capsys.readouterr().out)
    assert payload['passed'] is True
    assert payload['canonical_candidate_count']>=10
