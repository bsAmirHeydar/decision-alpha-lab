from pathlib import Path
import json,sys
o=json.loads(Path(sys.argv[1]).read_text()); req={"system_id","claims","evidence","limitations","independent_reviewer"}; m=req-set(o);
if m: raise SystemExit(f"missing {m}")
if not o["limitations"]: raise SystemExit("limitations required")
print({"status":"structurally_valid","claims":len(o["claims"])})
