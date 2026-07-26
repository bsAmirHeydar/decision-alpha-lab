import json
from jsonschema import Draft202012Validator
def test_all_schemas_are_valid(repo_root):
    root=repo_root/'registry/history/acl/acl_06/schemas/v1'; files=list(root.glob('*.json')); assert len(files)>=20
    for p in files: Draft202012Validator.check_schema(json.loads(p.read_text()))
def test_policies_are_machine_readable(repo_root):
    files=list((repo_root/'registry/history/acl/acl_06/policies/v1').glob('*.json')); assert len(files)>=18
    for p in files: assert json.loads(p.read_text())['policy_id'].startswith('ACL06_')
def test_obsidian_layers_exist(repo_root):
    assert (repo_root/'docs/architecture/master/context_lifecycle_os/12_PHASE_DELIVERIES/ACL_06/00_MOC.md').is_file()
    assert (repo_root/'docs/architecture/master/context_lifecycle_os/13_ATOMIC_CONCEPTS/ACL_06/00_MOC.md').is_file()
def test_mql_static_contracts_exist(repo_root): assert len(list((repo_root/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/ACL06').glob('*.mqh')))>=10
