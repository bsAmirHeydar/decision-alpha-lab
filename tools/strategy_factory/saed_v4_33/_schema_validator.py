class SchemaError(AssertionError): pass
def validate(value,schema,path="$"):
 kind=schema.get("type")
 if kind=="object":
  if not isinstance(value,dict): raise SchemaError(f"{path} not object")
  missing=set(schema.get("required",[]))-set(value)
  if missing: raise SchemaError(f"{path} missing {sorted(missing)}")
  props=schema.get("properties",{})
  if schema.get("additionalProperties") is False:
   unknown=set(value)-set(props)
   if unknown: raise SchemaError(f"{path} unknown {sorted(unknown)}")
  for k,v in value.items():
   if k in props: validate(v,props[k],f"{path}.{k}")
 elif kind=="array":
  if not isinstance(value,list): raise SchemaError(f"{path} not array")
  for i,v in enumerate(value): validate(v,schema.get("items",{}),f"{path}[{i}]")
 elif kind=="string" and not isinstance(value,str): raise SchemaError(f"{path} not string")
 elif kind=="integer" and (not isinstance(value,int) or isinstance(value,bool)): raise SchemaError(f"{path} not integer")
 elif kind=="number" and (not isinstance(value,(int,float)) or isinstance(value,bool)): raise SchemaError(f"{path} not number")
 elif kind=="boolean" and not isinstance(value,bool): raise SchemaError(f"{path} not boolean")
 elif kind=="null" and value is not None: raise SchemaError(f"{path} not null")
