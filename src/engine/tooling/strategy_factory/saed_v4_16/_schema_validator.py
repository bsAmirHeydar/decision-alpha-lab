def validate(v,s,path='$'):
 t=s.get('type')
 if t=='object':
  assert isinstance(v,dict),path;assert set(v)==set(s.get('required',[])),(path,set(v)^set(s.get('required',[])))
  for k in v:validate(v[k],s['properties'][k],path+'.'+k)
 elif t=='array':
  assert isinstance(v,list),path
  for i,x in enumerate(v):validate(x,s.get('items',{}),f'{path}[{i}]')
 elif t=='boolean':assert isinstance(v,bool),path
 elif t=='integer':assert isinstance(v,int) and not isinstance(v,bool),path
 elif t=='number':assert isinstance(v,(int,float)) and not isinstance(v,bool),path
 elif t=='null':assert v is None,path
 elif t=='string':assert isinstance(v,str),path
