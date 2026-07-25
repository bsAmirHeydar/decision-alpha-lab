from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__); TOOL=Path(__file__).resolve().parent
if str(TOOL) not in sys.path: sys.path.insert(0,str(TOOL))
from _schema_validator import validate,closed_objects
EX=ROOT/"examples/legacy/strategy_factory/saed_v4_28"; AR=ROOT/"releases/history/strategy_factory/artifacts/saed_v4_28"; SC=ROOT/"schemas/legacy/strategy_factory/saed_v4_28"
files=sorted(EX.glob("*.JSON"))+sorted(AR.glob("*.JSON"))
for p in files:
    sp=SC/(p.stem+".SCHEMA.JSON"); assert sp.is_file(),sp; schema=json.loads(sp.read_text(encoding="utf-8")); assert closed_objects(schema),sp; validate(p,sp)
assert len(list(SC.glob("*.SCHEMA.JSON")))==len(files)
print(f"V4-28 closed contracts passed: {len(files)} schema pairs")
