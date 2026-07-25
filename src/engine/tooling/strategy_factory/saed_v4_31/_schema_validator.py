from __future__ import annotations
from typing import Any

def validate(value:Any,schema:dict,path:str="$",reject_unknown:bool=True)->None:
    kind=schema.get("type")
    if kind=="object":
        assert isinstance(value,dict),f"{path} must be object"
        required=set(schema.get("required",[])); props=schema.get("properties",{})
        assert required.issubset(value),f"{path} missing {sorted(required-set(value))}"
        if reject_unknown and schema.get("additionalProperties") is False: assert set(value).issubset(props),f"{path} unknown {sorted(set(value)-set(props))}"
        for key,item in value.items():
            if key in props: validate(item,props[key],f"{path}.{key}",reject_unknown)
    elif kind=="array":
        assert isinstance(value,list),f"{path} must be array"
        for index,item in enumerate(value): validate(item,schema.get("items",{}),f"{path}[{index}]",reject_unknown)
    elif kind=="boolean": assert isinstance(value,bool),f"{path} must be bool"
    elif kind=="integer": assert isinstance(value,int) and not isinstance(value,bool),f"{path} must be integer"
    elif kind=="number": assert isinstance(value,(int,float)) and not isinstance(value,bool),f"{path} must be number"
    elif kind=="null": assert value is None,f"{path} must be null"
    elif kind=="string": assert isinstance(value,str),f"{path} must be string"
