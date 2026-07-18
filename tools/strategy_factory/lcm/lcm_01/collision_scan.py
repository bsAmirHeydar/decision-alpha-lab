from __future__ import annotations
from collections import defaultdict
import re

def scan(records: tuple[dict,...], long_threshold: int) -> dict:
    bycase=defaultdict(list); reserved=[]; trailing=[]; long=[]
    reserved_names={'con','prn','aux','nul'}|{f'com{i}' for i in range(1,10)}|{f'lpt{i}' for i in range(1,10)}
    for r in records:
        path=r['path']; bycase[path.casefold()].append(path)
        for part in path.split('/'):
            base=part.split('.',1)[0].casefold()
            if base in reserved_names: reserved.append(path); break
            if part.endswith((' ','.')): trailing.append(path); break
        if len(path)>long_threshold: long.append({'path':path,'path_length':len(path),'threshold':long_threshold})
    collisions=[{'casefold_path':k,'paths':sorted(v),'member_count':len(v)} for k,v in sorted(bycase.items()) if len(v)>1]
    return {'case_insensitive_collisions':collisions,'windows_reserved_name_paths':sorted(set(reserved)),'trailing_dot_or_space_paths':sorted(set(trailing)),'long_windows_paths':sorted(long,key=lambda x:(-x['path_length'],x['path']))}
