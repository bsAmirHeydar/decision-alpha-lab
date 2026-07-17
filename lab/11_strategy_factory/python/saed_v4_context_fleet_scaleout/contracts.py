from __future__ import annotations
from typing import Any,Iterable
from .errors import ContractError
def exact(v:dict[str,Any],required:Iterable[str],optional:Iterable[str]=(),name:str="contract"):
 if not isinstance(v,dict):raise ContractError(f"{name} must be object")
 req=set(required);allowed=req|set(optional);missing=sorted(req-set(v));unknown=sorted(set(v)-allowed)
 if missing or unknown:raise ContractError(f"{name} missing={missing} unknown={unknown}")
def list_of(v:Any,name:str,minimum:int=0)->list:
 if not isinstance(v,list) or len(v)<minimum:raise ContractError(f"{name} invalid")
 return v
def unique(items:list[dict],field:str,name:str):
 vals=[x.get(field) for x in items]
 if None in vals or len(vals)!=len(set(vals)):raise ContractError(f"{name} duplicate/missing {field}")
def boolean(v:Any,name:str,expected:bool|None=None)->bool:
 if not isinstance(v,bool):raise ContractError(f"{name} must be bool")
 if expected is not None and v is not expected:raise ContractError(f"{name} must be {expected}")
 return v
def number(v:Any,name:str,minimum:float|None=None,maximum:float|None=None)->float:
 if not isinstance(v,(int,float)) or isinstance(v,bool):raise ContractError(f"{name} invalid")
 x=float(v)
 if minimum is not None and x<minimum:raise ContractError(f"{name} below minimum")
 if maximum is not None and x>maximum:raise ContractError(f"{name} above maximum")
 return x
def integer(v:Any,name:str,minimum:int=0,maximum:int|None=None)->int:
 if not isinstance(v,int) or isinstance(v,bool) or v<minimum or (maximum is not None and v>maximum):raise ContractError(f"{name} invalid")
 return v
def enum(v:Any,allowed:set[str],name:str)->str:
 if v not in allowed:raise ContractError(f"{name} invalid: {v}")
 return v
def sha256(v:Any,name:str)->str:
 if not isinstance(v,str) or len(v)!=64 or any(c not in '0123456789abcdef' for c in v):raise ContractError(f"{name} must be lowercase sha256")
 return v
def sorted_unique_strings(v:Any,name:str,minimum:int=0)->list[str]:
 xs=list_of(v,name,minimum)
 if any(not isinstance(x,str) or not x for x in xs) or xs!=sorted(set(xs)):raise ContractError(f"{name} must be sorted unique strings")
 return xs
