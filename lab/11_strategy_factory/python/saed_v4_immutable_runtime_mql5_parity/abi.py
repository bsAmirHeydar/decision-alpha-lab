from __future__ import annotations
from copy import deepcopy
from .contracts import exact,list_of,unique,enum,integer,number,sorted_unique_strings
from .errors import ABIError
from .canonical import content_hash,seal
TYPES={"FLOAT64","INT64","BOOL","ENUM","STRING"}; DIRECTIONS={"INPUT","OUTPUT","STATE"}

def _freeze_fields(fields:list[dict],kind:str)->list[dict]:
 fields=list_of(fields,kind,1); unique(fields,"field_id",kind); out=[]
 for f in fields:
  exact(f,["field_id","ordinal","name","data_type","direction","required","default","minimum","maximum","enum_values","semantic","unit"])
  integer(f["ordinal"],"ordinal",0); enum(f["data_type"],TYPES,"data_type"); enum(f["direction"],DIRECTIONS,"direction")
  if not isinstance(f["required"],bool):raise ABIError("required must be bool")
  if f["data_type"] in {"FLOAT64","INT64"}:
   number(f["minimum"],"minimum"); number(f["maximum"],"maximum")
   if f["minimum"]>f["maximum"]:raise ABIError("field bounds invalid")
  if f["data_type"]=="ENUM":sorted_unique_strings(f["enum_values"],"enum_values",1)
  else:
   if f["enum_values"]!=[]:raise ABIError("enum_values only valid for ENUM")
  x=deepcopy(f); x["field_hash"]=content_hash(x); out.append(x)
 out=sorted(out,key=lambda z:z["ordinal"])
 if [x["ordinal"] for x in out]!=list(range(len(out))):raise ABIError(f"{kind} ordinals must be contiguous")
 return out

def freeze_abi(v:dict,kind:str)->dict:
 exact(v,["abi_id","version","kind","fields","closed_contract","backward_compatible_with","research_only"])
 if v["kind"]!=kind or v["closed_contract"] is not True or v["research_only"] is not True:raise ABIError("ABI boundary invalid")
 fields=_freeze_fields(v["fields"],kind)
 return seal({**deepcopy(v),"fields":fields,"field_count":len(fields),"abi_hash":content_hash({"kind":kind,"fields":fields,"version":v["version"]})},f"v438_{kind.lower()}_abi","frozen_abi_id","frozen_abi_hash")

def freeze_all(feature:dict,model:dict,policy:dict,output:dict,state:dict)->dict:
 items=[freeze_abi(feature,"FEATURE"),freeze_abi(model,"MODEL"),freeze_abi(policy,"POLICY"),freeze_abi(output,"OUTPUT"),freeze_abi(state,"STATE")]
 return seal({"phase":"SAED_V4_38","abis":items,"abi_hashes":[x["abi_hash"] for x in items],"research_only":True},"v438_abis","registry_id","registry_hash")
