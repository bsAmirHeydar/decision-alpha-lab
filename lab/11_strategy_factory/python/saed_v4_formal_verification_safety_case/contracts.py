from __future__ import annotations
from typing import Any,Iterable
from .errors import ContractError

def require_exact(value:dict[str,Any],required:Iterable[str],optional:Iterable[str]=(),name:str="contract")->None:
    if not isinstance(value,dict): raise ContractError(f"{name} must be object")
    required=set(required); allowed=required|set(optional); keys=set(value)
    missing=sorted(required-keys); unknown=sorted(keys-allowed)
    if missing or unknown: raise ContractError(f"{name} missing={missing} unknown={unknown}")

def require_list(value:Any,name:str,minimum:int=0)->list:
    if not isinstance(value,list) or len(value)<minimum: raise ContractError(f"{name} invalid")
    return value

def require_unique(items:list[dict],field:str,name:str)->None:
    values=[x.get(field) for x in items]
    if None in values or len(values)!=len(set(values)): raise ContractError(f"{name} duplicate or missing {field}")

def require_bool_false(value:Any,name:str)->None:
    if value is not False: raise ContractError(f"{name} must be false")

def require_sha256(value:Any,name:str)->str:
    if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):
        raise ContractError(f"{name} must be lowercase sha256")
    return value
