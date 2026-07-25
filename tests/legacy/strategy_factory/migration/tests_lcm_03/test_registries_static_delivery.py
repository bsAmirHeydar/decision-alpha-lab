import json
from tools.strategy_factory.lcm.lcm_03.delivery_validation import validate_file_index
from tools.strategy_factory.lcm.lcm_03.schema_validation import validate_schemas
from tools.strategy_factory.lcm.lcm_03.static_validation import run

def test_schemas(repo_root): assert validate_schemas(repo_root/'registry/legacy_context_migration/lcm_03/schemas/v1')>=20
def test_policies_parse(repo_root):
    files=list((repo_root/'registry/legacy_context_migration/lcm_03/policies/v1').glob('*.json'));assert len(files)>=20;[json.loads(x.read_text()) for x in files]
def test_static(repo_root): assert run(repo_root)['passed']
def test_file_index(repo_root): assert validate_file_index(repo_root,repo_root/'releases/history/lcm/indexes/LCM_03_FILE_INDEX.txt')['passed']
def test_docs(repo_root): assert len(list((repo_root/'docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/11_PHASE_DELIVERIES/LCM_03').glob('*.md')))>=40
def test_mql_contracts(repo_root): assert len(list((repo_root/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/LCM/LCM03').glob('*.mqh')))>=10
