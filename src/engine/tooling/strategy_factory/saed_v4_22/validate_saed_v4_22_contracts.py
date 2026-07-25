from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__);sys.path.insert(0,str(Path(__file__).parent))
from _schema_validator import validate
schema=ROOT/'schemas/legacy/strategy_factory/saed_v4_22';count=0
for d in [ROOT/'examples/legacy/strategy_factory/saed_v4_22',ROOT/'releases/history/strategy_factory/artifacts/saed_v4_22']:
    for p in sorted(d.glob('*.JSON')):
        s=schema/(p.stem+'.SCHEMA.JSON')
        if not s.exists():raise SystemExit(f'missing schema for {p.name}')
        validate(json.loads(p.read_text()),json.loads(s.read_text()));count+=1
print(json.dumps({'passed':True,'validated_documents':count,'closed_schemas':len(list(schema.glob("*.SCHEMA.JSON")))},sort_keys=True))
