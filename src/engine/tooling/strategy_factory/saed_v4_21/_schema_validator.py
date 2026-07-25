class SchemaError(AssertionError):pass
def validate(v,s,path='$'):
 t=s.get('type')
 ok={'object':isinstance(v,dict),'array':isinstance(v,list),'string':isinstance(v,str),'integer':isinstance(v,int) and not isinstance(v,bool),'number':isinstance(v,(int,float)) and not isinstance(v,bool),'boolean':isinstance(v,bool),'null':v is None}.get(t,True)
 if not ok:raise SchemaError(f'{path}: expected {t}, got {type(v).__name__}')
 if t=='object':
  req=set(s.get('required',[]));props=s.get('properties',{});missing=req-set(v)
  if missing:raise SchemaError(f'{path}: missing {sorted(missing)}')
  if s.get('additionalProperties') is False:
   extra=set(v)-set(props)
   if extra:raise SchemaError(f'{path}: extra {sorted(extra)}')
  for k,x in v.items():
   if k in props:validate(x,props[k],f'{path}.{k}')
 if t=='array' and 'items' in s:
  for i,x in enumerate(v):validate(x,s['items'],f'{path}[{i}]')
 return True
