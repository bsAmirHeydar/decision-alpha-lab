from __future__ import annotations
import json
from pathlib import Path
def validate_schema_directory(root:Path)->dict:
    files=sorted(root.glob("*.schema.json")); failures=[]
    for p in files:
        try:
            d=json.loads(p.read_text())
            if d.get("$schema")!="https://json-schema.org/draft/2020-12/schema" or d.get("type")!="object": failures.append(p.name)
        except Exception: failures.append(p.name)
    if failures: raise RuntimeError("invalid schemas: "+str(failures))
    return {"passed":True,"schema_count":len(files)}
