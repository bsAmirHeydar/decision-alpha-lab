import json
from pathlib import Path
from tools.strategy_factory.lcm.lcm_08a.schema_validation import validate
from tools.strategy_factory.lcm.lcm_08a.static_validation import scan

ROOT=Path(__file__).resolve().parents[4]

def test_schemas_are_draft_2020_12_valid():
    result=validate(ROOT/'registry/legacy_context_migration/lcm_08a/schemas/v1')
    assert result['passed']
    assert result['schema_count']>=13

def test_mql_static_mirror_has_no_order_api():
    findings=scan(ROOT/'lab/11_strategy_factory/mql5/Include/AlphaLab/ACL_OS/LCM08A')
    assert findings==[]

def test_phase_doc_is_implemented_reference():
    path=ROOT/'docs/alpha_lab_master_architecture/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_08A_CONTEXT_PORTFOLIO_FREEZE_RISK_CLASSIFICATION_AND_PILOT_SELECTION.md'
    text=path.read_text(encoding='utf-8')
    assert 'status: implemented-reference' in text
    assert 'No source path is moved' in text
