from __future__ import annotations
from typing import Any,Iterable
from .errors import ContractError

def require_exact(value:dict[str,Any],required:Iterable[str],optional:Iterable[str]=(),name:str="contract")->None:
    if not isinstance(value,dict): raise ContractError(f"{name} must be object")
    req=set(required); allowed=req|set(optional); keys=set(value)
    missing=sorted(req-keys); unknown=sorted(keys-allowed)
    if missing or unknown: raise ContractError(f"{name} missing={missing} unknown={unknown}")

def require_list(value:Any,name:str,minimum:int=0)->list:
    if not isinstance(value,list) or len(value)<minimum: raise ContractError(f"{name} invalid")
    return value

def require_unique(items:list[dict],field:str,name:str)->None:
    values=[x.get(field) for x in items]
    if None in values or len(values)!=len(set(values)): raise ContractError(f"{name} duplicate or missing {field}")

def require_enum(value:Any,allowed:set[str],name:str)->str:
    if value not in allowed: raise ContractError(f"{name} must be one of {sorted(allowed)}")
    return value

def require_bool(value:Any,name:str,expected:bool|None=None)->bool:
    if not isinstance(value,bool): raise ContractError(f"{name} must be boolean")
    if expected is not None and value is not expected: raise ContractError(f"{name} must be {expected}")
    return value

def require_nonnegative_int(value:Any,name:str)->int:
    if not isinstance(value,int) or isinstance(value,bool) or value<0: raise ContractError(f"{name} must be nonnegative integer")
    return value

def require_positive_int(value:Any,name:str)->int:
    if not isinstance(value,int) or isinstance(value,bool) or value<=0: raise ContractError(f"{name} must be positive integer")
    return value

def require_sha256(value:Any,name:str)->str:
    if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):
        raise ContractError(f"{name} must be lowercase sha256")
    return value

def require_sorted_unique_strings(value:Any,name:str)->list[str]:
    xs=require_list(value,name)
    if any(not isinstance(x,str) or not x for x in xs): raise ContractError(f"{name} must contain nonempty strings")
    if xs!=sorted(set(xs)): raise ContractError(f"{name} must be sorted unique")
    return xs
