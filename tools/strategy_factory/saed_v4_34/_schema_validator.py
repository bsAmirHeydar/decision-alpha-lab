from __future__ import annotations
class ValidationError(Exception):pass

def validate(value,schema,path="$",strict=True):
    t=schema.get("type")
    if t=="object":
        if not isinstance(value,dict):raise ValidationError(f"{path} not object")
        req=set(schema.get("required",[]));missing=req-set(value)
        if missing:raise ValidationError(f"{path} missing {sorted(missing)}")
        props=schema.get("properties",{})
        if schema.get("additionalProperties") is False:
            extra=set(value)-set(props)
            if extra:raise ValidationError(f"{path} extra {sorted(extra)}")
        for k,v in value.items():
            if k in props:validate(v,props[k],f"{path}.{k}",strict)
    elif t=="array":
        if not isinstance(value,list):raise ValidationError(f"{path} not array")
        for i,v in enumerate(value):validate(v,schema.get("items",{}),f"{path}[{i}]",strict)
    elif t=="string" and not isinstance(value,str):raise ValidationError(f"{path} not string")
    elif t=="integer" and (not isinstance(value,int) or isinstance(value,bool)):raise ValidationError(f"{path} not integer")
    elif t=="number" and (not isinstance(value,(int,float)) or isinstance(value,bool)):raise ValidationError(f"{path} not number")
    elif t=="boolean" and not isinstance(value,bool):raise ValidationError(f"{path} not boolean")
    elif t=="null" and value is not None:raise ValidationError(f"{path} not null")
