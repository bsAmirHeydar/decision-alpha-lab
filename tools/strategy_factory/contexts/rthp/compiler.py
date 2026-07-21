from __future__ import annotations
import hashlib,json
from pathlib import Path
import yaml
CONTRACTS=["scope","ontology","causal_clock","data","missingness","cycles","calendar","symbol_pair","price_basis","touch","state_machine","occurrence","references","signal_families","lookback","revisions","parity","visual_boundary","feature_views","treatment_envelope","acceptance_gates"]
def compile_package(root:Path)->dict:
 manifest=yaml.safe_load((root/"context_manifest.yaml").read_text(encoding="utf-8")); compiled={"manifest":manifest,"contracts":{},"extensions":{}}
 for key,path in manifest["contracts"].items():
  p=root/path
  if p.suffix in {".yaml",".yml"}:compiled["contracts"][key]=yaml.safe_load(p.read_text(encoding="utf-8"))
 ext=root/"contracts/rthp_extension_manifest.yaml"
 if ext.is_file():
  em=yaml.safe_load(ext.read_text(encoding="utf-8"))
  for key,path in em.get("contracts",{}).items():
   ep=root/path
   compiled["extensions"][key]=yaml.safe_load(ep.read_text(encoding="utf-8"))
 compiled["compiled_digest"]="sha256:"+hashlib.sha256(json.dumps(compiled,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest();return compiled
