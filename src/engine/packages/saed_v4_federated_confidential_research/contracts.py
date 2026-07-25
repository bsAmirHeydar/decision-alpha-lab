from __future__ import annotations
from typing import Any,Iterable
from .errors import ContractError

def require_exact(value:dict[str,Any],required:Iterable[str],optional:Iterable[str]=(),name:str="contract")->None:
    if not isinstance(value,dict): raise ContractError(f"{name} must be object")
    req=set(required); allowed=req|set(optional); missing=sorted(req-set(value)); unknown=sorted(set(value)-allowed)
    if missing or unknown: raise ContractError(f"{name} missing={missing} unknown={unknown}")

def require_list(value:Any,name:str,minimum:int=0)->list:
    if not isinstance(value,list) or len(value)<minimum: raise ContractError(f"{name} invalid")
    return value

def require_unique(items:list[dict],field:str,name:str)->None:
    vals=[x.get(field) for x in items]
    if None in vals or len(vals)!=len(set(vals)): raise ContractError(f"{name} duplicate or missing {field}")

def require_sorted_unique_strings(value:Any,name:str)->list[str]:
    xs=require_list(value,name)
    if any(not isinstance(x,str) or not x for x in xs) or xs!=sorted(set(xs)): raise ContractError(f"{name} must be sorted unique strings")
    return xs

def require_bool(v:Any,name:str,expected:bool|None=None)->bool:
    if not isinstance(v,bool): raise ContractError(f"{name} must be boolean")
    if expected is not None and v is not expected: raise ContractError(f"{name} must be {expected}")
    return v

def require_nonnegative(v:Any,name:str)->float:
    if not isinstance(v,(int,float)) or isinstance(v,bool) or v<0: raise ContractError(f"{name} must be nonnegative")
    return float(v)

def require_positive_int(v:Any,name:str)->int:
    if not isinstance(v,int) or isinstance(v,bool) or v<=0: raise ContractError(f"{name} must be positive integer")
    return v

def require_sha256(v:Any,name:str)->str:
    if not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v): raise ContractError(f"{name} must be lowercase sha256")
    return v
