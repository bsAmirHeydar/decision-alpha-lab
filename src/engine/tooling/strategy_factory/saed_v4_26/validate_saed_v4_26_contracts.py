from tools.repository_paths import find_repository_root
from pathlib import Path
import json,sys
ROOT=find_repository_root(__file__); sys.path.insert(0,str(ROOT/"src/engine/tooling/strategy_factory/saed_v4_26"))
from _schema_validator import closed_objects,validate
pairs=[]
for d in [ROOT/"examples/legacy/strategy_factory/saed_v4_26",ROOT/"releases/history/strategy_factory/artifacts/saed_v4_26"]:
 for p in sorted(d.glob("*.JSON")):
  s=ROOT/"schemas/legacy/strategy_factory/saed_v4_26"/f"{p.stem}.SCHEMA.JSON"; assert s.is_file(); validate(p,s); value=json.loads(s.read_text()); assert closed_objects(value); assert value["x-phase"]=="SAED_V4_26" and value["x-authority"]=="research-only-nonproduction"; pairs.append((p,s))
assert len(pairs)==39 and len(list((ROOT/"schemas/legacy/strategy_factory/saed_v4_26").glob("*.SCHEMA.JSON")))==39
print("V4-26 contract validation passed: 39 closed schema pairs")
