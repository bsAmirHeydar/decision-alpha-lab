from tools.repository_paths import find_repository_root
import json
from pathlib import Path
from src.engine.tooling.strategy_factory.lcm.lcm_08a.schema_validation import validate
from src.engine.tooling.strategy_factory.lcm.lcm_08a.static_validation import scan

ROOT=find_repository_root(__file__)

def test_schemas_are_draft_2020_12_valid():
    result=validate(ROOT/'registry/history/lcm/lcm_08a/schemas/v1')
    assert result['passed']
    assert result['schema_count']>=13

def test_mql_static_mirror_has_no_order_api():
    findings=scan(ROOT/'mql5/legacy/strategy_factory_lab/Include/AlphaLab/ACL_OS/LCM08A')
    assert findings==[]

def test_phase_doc_is_implemented_reference():
    path=ROOT/'docs/architecture/master/context_lifecycle_os/17_LEGACY_MIGRATION_PROGRAM/05_PHASES/LCM_08A_CONTEXT_PORTFOLIO_FREEZE_RISK_CLASSIFICATION_AND_PILOT_SELECTION.md'
    text=path.read_text(encoding='utf-8')
    assert 'status: implemented-reference' in text
    assert 'No source path is moved' in text
