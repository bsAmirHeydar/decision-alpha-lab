def validate(v,s,path='$'):
    t=s.get('type')
    if t=='object':
        if not isinstance(v,dict):raise AssertionError(f'{path}: expected object')
        req=set(s.get('required',[]));props=s.get('properties',{})
        if not req<=set(v):raise AssertionError(f'{path}: missing fields {sorted(req-set(v))}')
        if s.get('additionalProperties') is False and not set(v)<=set(props):raise AssertionError(f'{path}: unknown fields')
        for k,x in v.items():validate(x,props[k],f'{path}.{k}')
    elif t=='array':
        if not isinstance(v,list):raise AssertionError(f'{path}: expected array')
        for i,x in enumerate(v):validate(x,s.get('items',{}),f'{path}[{i}]')
    elif t=='boolean' and not isinstance(v,bool):raise AssertionError(f'{path}: expected boolean')
    elif t=='integer' and (not isinstance(v,int) or isinstance(v,bool)):raise AssertionError(f'{path}: expected integer')
    elif t=='number' and (not isinstance(v,(int,float)) or isinstance(v,bool)):raise AssertionError(f'{path}: expected number')
    elif t=='string' and not isinstance(v,str):raise AssertionError(f'{path}: expected string')
    elif t=='null' and v is not None:raise AssertionError(f'{path}: expected null')
