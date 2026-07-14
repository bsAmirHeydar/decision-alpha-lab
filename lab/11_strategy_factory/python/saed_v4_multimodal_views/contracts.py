from __future__ import annotations
import json
from pathlib import Path
from typing import Any,Mapping
import yaml
from jsonschema import Draft202012Validator,FormatChecker
from .errors import ContractError

def load_document(path:str|Path)->Any:
    p=Path(path);s=p.suffix.lower()
    if s in {'.yaml','.yml'}:return yaml.safe_load(p.read_text(encoding='utf-8'))
    if s=='.json':return json.loads(p.read_text(encoding='utf-8'))
    raise ContractError(f'unsupported extension: {s}')
def validate_closed(document:Any,schema:Mapping[str,Any])->None:
    errors=sorted(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(document),key=lambda e:list(e.absolute_path))
    if errors:raise ContractError('; '.join(f"{'.'.join(map(str,e.absolute_path)) or '$'}: {e.message}" for e in errors[:40]))
