from __future__ import annotations
import json
from pathlib import Path
try:
    from jsonschema import Draft202012Validator
except Exception: Draft202012Validator=None
def validate_schema_file(path:Path)->list[str]:
    try: obj=json.loads(path.read_text(encoding='utf-8'))
    except Exception as e: return [str(e)]
    if Draft202012Validator is None: return []
    try: Draft202012Validator.check_schema(obj); return []
    except Exception as e: return [str(e)]
