from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'tools/strategy_factory/saed_v4_24'))
from _schema_validator import validate
EX = ROOT / 'lab/11_strategy_factory/examples/saed_v4_24'
ART = ROOT / 'lab/11_strategy_factory/artifacts/saed_v4_24'
SCH = ROOT / 'lab/11_strategy_factory/schemas/saed_v4_24'
count = 0
for schema_path in sorted(SCH.glob('*.SCHEMA.JSON')):
    stem = schema_path.name.replace('.SCHEMA.JSON', '')
    source = EX / f'{stem}.JSON' if (EX / f'{stem}.JSON').is_file() else ART / f'{stem}.JSON'
    assert source.is_file(), stem
    validate(json.loads(source.read_text()), json.loads(schema_path.read_text()))
    count += 1
print(f'V4-24 closed contracts passed: {count} document/schema pairs')
