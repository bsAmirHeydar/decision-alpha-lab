from tools.repository_paths import find_repository_root
from pathlib import Path
import json
import sys
import pytest
ROOT = find_repository_root(__file__)
sys.path.insert(0, str(ROOT / 'src/engine/tooling/strategy_factory/saed_v4_24'))
from _schema_validator import validate
EX = ROOT / 'examples/legacy/strategy_factory/saed_v4_24'
ART = ROOT / 'releases/history/strategy_factory/artifacts/saed_v4_24'
SCH = ROOT / 'schemas/legacy/strategy_factory/saed_v4_24'
STEMS = [path.name.replace('.SCHEMA.JSON', '') for path in sorted(SCH.glob('*.SCHEMA.JSON'))]
@pytest.mark.parametrize('stem', STEMS)
def test_closed_schema_pair(stem):
    source = EX / f'{stem}.JSON' if (EX / f'{stem}.JSON').is_file() else ART / f'{stem}.JSON'
    validate(json.loads(source.read_text()), json.loads((SCH / f'{stem}.SCHEMA.JSON').read_text()))
@pytest.mark.parametrize('stem', STEMS[:24])
def test_unknown_root_field_rejected(stem):
    source = EX / f'{stem}.JSON' if (EX / f'{stem}.JSON').is_file() else ART / f'{stem}.JSON'
    instance = json.loads(source.read_text()); schema = json.loads((SCH / f'{stem}.SCHEMA.JSON').read_text())
    if isinstance(instance, dict):
        instance['unknown_field'] = 1
        with pytest.raises(AssertionError): validate(instance, schema)
