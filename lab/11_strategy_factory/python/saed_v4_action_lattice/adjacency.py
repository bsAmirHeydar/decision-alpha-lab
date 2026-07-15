def assignment_distance(a:dict,b:dict)->int:
    keys=set(a)|set(b);return sum(a.get(k)!=b.get(k) for k in keys)
