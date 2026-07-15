def validate(value,schema,path='$'):
 t=schema.get('type')
 if 'anyOf' in schema:
  errs=[]
  for s in schema['anyOf']:
   try:validate(value,s,path);return
   except Exception as e:errs.append(str(e))
  raise AssertionError(f'{path}: no anyOf branch matched')
 if t=='object':
  assert isinstance(value,dict),f'{path}: expected object';req=set(schema.get('required',[]));assert set(value)==req,f'{path}: fields mismatch {sorted(set(value)^req)}'
  for k in req:validate(value[k],schema['properties'][k],path+'.'+k)
 elif t=='array':
  assert isinstance(value,list),f'{path}: expected array'
  for i,x in enumerate(value):validate(x,schema.get('items',{}),f'{path}[{i}]')
 elif t=='string':assert isinstance(value,str),f'{path}: expected string'
 elif t=='boolean':assert isinstance(value,bool),f'{path}: expected boolean'
 elif t=='integer':assert isinstance(value,int) and not isinstance(value,bool),f'{path}: expected integer'
 elif t=='number':assert isinstance(value,(int,float)) and not isinstance(value,bool),f'{path}: expected number'
 elif t=='null':assert value is None,f'{path}: expected null'
