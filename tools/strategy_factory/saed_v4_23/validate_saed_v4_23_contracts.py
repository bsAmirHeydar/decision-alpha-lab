from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(Path(__file__).parent))
from _schema_validator import validate
roots=[ROOT/'lab/11_strategy_factory/examples/saed_v4_23',ROOT/'lab/11_strategy_factory/artifacts/saed_v4_23'];sch=ROOT/'lab/11_strategy_factory/schemas/saed_v4_23';count=0
for folder in roots:
    for p in sorted(folder.glob('*.JSON')):
        s=sch/f'{p.stem}.SCHEMA.JSON';assert s.is_file(),p.name;validate(json.loads(p.read_text(encoding='utf-8')),json.loads(s.read_text(encoding='utf-8')));count+=1
assert count==len(list(sch.glob('*.SCHEMA.JSON')))
print(f'V4-23 closed contract validation passed: {count} document/schema pairs')
