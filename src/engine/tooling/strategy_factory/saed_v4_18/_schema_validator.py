def validate(value,schema,path='$'):
 t=schema.get('type')
 if 'anyOf' in schema:
  errors=[]
  for candidate in schema['anyOf']:
   try:validate(value,candidate,path);return True
   except AssertionError as e:errors.append(str(e))
  raise AssertionError(f'{path}: no anyOf schema matched')
 if t=='object':
  assert isinstance(value,dict),f'{path}: expected object'
  required=set(schema.get('required',[]));assert required<=set(value),f'{path}: missing {sorted(required-set(value))}'
  if schema.get('additionalProperties') is False:assert set(value)<=set(schema.get('properties',{})),f'{path}: unknown {sorted(set(value)-set(schema.get("properties",{})))}'
  for k,s in schema.get('properties',{}).items():
   if k in value:validate(value[k],s,f'{path}.{k}')
 elif t=='array':
  assert isinstance(value,list),f'{path}: expected array'
  for i,x in enumerate(value):validate(x,schema.get('items',{}),f'{path}[{i}]')
 elif t=='string':assert isinstance(value,str),f'{path}: expected string'
 elif t=='integer':assert isinstance(value,int) and not isinstance(value,bool),f'{path}: expected integer'
 elif t=='number':assert isinstance(value,(int,float)) and not isinstance(value,bool),f'{path}: expected number'
 elif t=='boolean':assert isinstance(value,bool),f'{path}: expected boolean'
 elif t=='null':assert value is None,f'{path}: expected null'
 return True
