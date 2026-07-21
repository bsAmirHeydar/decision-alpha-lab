from __future__ import annotations
import json
from pathlib import Path
def validate_schema_catalog(root:Path)->dict:
    errors=[];files=sorted(root.glob("*.schema.json"))
    for p in files:
        try:
            v=json.loads(p.read_text(encoding="utf-8"))
            if v.get("$schema")!="https://json-schema.org/draft/2020-12/schema":errors.append({"path":p.as_posix(),"error":"DRAFT_MISMATCH"})
            if v.get("type")!="object":errors.append({"path":p.as_posix(),"error":"ROOT_NOT_OBJECT"})
        except Exception as exc:errors.append({"path":p.as_posix(),"error":str(exc)})
    return {"result":"PASS" if files and not errors else "FAIL","schema_count":len(files),"errors":errors}
