from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[3]
TOOL=Path(__file__).resolve().parent
if str(TOOL) not in sys.path: sys.path.insert(0,str(TOOL))
from _schema_validator import validate, closed_objects
EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_27"; AR=ROOT/"lab/11_strategy_factory/artifacts/saed_v4_27"; SC=ROOT/"lab/11_strategy_factory/schemas/saed_v4_27"
files=sorted(EX.glob("*.JSON"))+sorted(AR.glob("*.JSON"))
assert len(files)==25
for p in files:
    sp=SC/(p.stem+".SCHEMA.JSON"); assert sp.is_file(),sp
    schema=json.loads(sp.read_text(encoding="utf-8")); assert closed_objects(schema),sp
    validate(p,sp)
assert len(list(SC.glob("*.SCHEMA.JSON")))==25
print("V4-27 closed contracts passed: 25 schema pairs")
