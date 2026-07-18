from __future__ import annotations
import json
from typing import Any
from jsonschema import Draft202012Validator,FormatChecker
from .errors import ContractError
from .policies import SCHEMA_ROOT
def load_schema(name:str)->dict:
    p=SCHEMA_ROOT/f'{name}.schema.json'
    if not p.is_file(): raise ContractError(f'ACL13_SCHEMA_NOT_REGISTERED:{name}')
    return json.loads(p.read_text(encoding='utf-8'))
def validate_instance(name:str,instance:Any)->None:
    schema=load_schema(name); Draft202012Validator.check_schema(schema)
    errors=sorted(Draft202012Validator(schema,format_checker=FormatChecker()).iter_errors(instance),key=lambda e:list(e.absolute_path))
    if errors: raise ContractError('ACL13_SCHEMA_REJECTED:'+'; '.join(e.message for e in errors[:6]))
