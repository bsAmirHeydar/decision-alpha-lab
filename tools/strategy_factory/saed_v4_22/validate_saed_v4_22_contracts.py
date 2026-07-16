from pathlib import Path
import json,sys
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(Path(__file__).parent))
from _schema_validator import validate
schema=ROOT/'lab/11_strategy_factory/schemas/saed_v4_22';count=0
for d in [ROOT/'lab/11_strategy_factory/examples/saed_v4_22',ROOT/'lab/11_strategy_factory/artifacts/saed_v4_22']:
    for p in sorted(d.glob('*.JSON')):
        s=schema/(p.stem+'.SCHEMA.JSON')
        if not s.exists():raise SystemExit(f'missing schema for {p.name}')
        validate(json.loads(p.read_text()),json.loads(s.read_text()));count+=1
print(json.dumps({'passed':True,'validated_documents':count,'closed_schemas':len(list(schema.glob("*.SCHEMA.JSON")))},sort_keys=True))
