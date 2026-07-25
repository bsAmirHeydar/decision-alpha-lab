def validate(v,s,path='$'):
    t=s.get('type')
    if t=='object':
        if not isinstance(v,dict):raise AssertionError(path+' not object')
        if set(v)!=set(s.get('required',[])):raise AssertionError(path+' fields mismatch')
        for k in s.get('required',[]):validate(v[k],s['properties'][k],path+'.'+k)
    elif t=='array':
        if not isinstance(v,list):raise AssertionError(path+' not array')
        for i,x in enumerate(v):validate(x,s.get('items',{}),f'{path}[{i}]')
    elif t=='boolean' and not isinstance(v,bool):raise AssertionError(path+' not boolean')
    elif t=='integer' and (not isinstance(v,int) or isinstance(v,bool)):raise AssertionError(path+' not integer')
    elif t=='number' and (not isinstance(v,(int,float)) or isinstance(v,bool)):raise AssertionError(path+' not number')
    elif t=='string' and not isinstance(v,str):raise AssertionError(path+' not string')
    elif t=='null' and v is not None:raise AssertionError(path+' not null')
    return True
