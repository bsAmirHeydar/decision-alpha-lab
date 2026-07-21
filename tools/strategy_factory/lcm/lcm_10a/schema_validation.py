from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator

def validate_schema_directory(root: Path) -> dict:
    failures=[]; files=sorted(root.glob('*.schema.json'))
    for path in files:
        try:
            doc=json.loads(path.read_text(encoding='utf-8')); Draft202012Validator.check_schema(doc)
            if doc.get('$schema')!='https://json-schema.org/draft/2020-12/schema': failures.append(path.name+':DRAFT')
        except Exception as exc: failures.append(path.name+':'+str(exc))
    if failures: raise RuntimeError('LCM10A_SCHEMA_VALIDATION_FAILED:'+str(failures[:10]))
    return {"passed":True,"schema_count":len(files)}
