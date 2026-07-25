from pathlib import Path
import csv,sys
p=Path(sys.argv[1]); rows=list(csv.DictReader(p.open(encoding="utf-8"))); required={"exposure_id","known_time","actor","artifact_hash","family_id"}; missing=required-set(rows[0] if rows else [])
if missing: raise SystemExit(f"missing columns {sorted(missing)}")
ids=[r["exposure_id"] for r in rows]
if len(ids)!=len(set(ids)): raise SystemExit("duplicate exposure_id")
print({"rows":len(rows),"status":"pass"})
