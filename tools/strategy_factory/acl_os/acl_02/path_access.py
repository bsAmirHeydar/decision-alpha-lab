from __future__ import annotations
from typing import Any
_MISSING=object()
def get_path(obj:Any,path:str,default:Any=_MISSING)->Any:
    cur=obj
    for token in path.split("."):
        if isinstance(cur,dict) and token in cur: cur=cur[token]
        elif isinstance(cur,list) and token.isdigit() and int(token)<len(cur): cur=cur[int(token)]
        else:
            if default is _MISSING: raise KeyError(path)
            return default
    return cur
