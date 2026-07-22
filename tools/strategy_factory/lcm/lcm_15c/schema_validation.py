from __future__ import annotations
import json
from pathlib import Path
def validate_schemas(schema_root:Path)->int:
 count=0
 for path in sorted(schema_root.glob('*.json')):
  obj=json.loads(path.read_text(encoding='utf-8'))
  if obj.get('$schema')!='https://json-schema.org/draft/2020-12/schema':raise ValueError(path)
  count+=1
 if count<13:raise ValueError('insufficient schemas')
 return count
