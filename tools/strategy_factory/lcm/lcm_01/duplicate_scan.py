from __future__ import annotations
from collections import defaultdict

def exact_duplicates(records: tuple[dict,...]) -> list[dict]:
    groups=defaultdict(list)
    for r in records:
        if r['kind']=='FILE': groups[(r['sha256'],r['size_bytes'])].append(r['path'])
    out=[]
    for (digest,size),paths in sorted(groups.items()):
        if len(paths)>1:
            out.append({'sha256':digest,'size_bytes':size,'member_count':len(paths),'paths':sorted(paths),'semantic_equivalence_claimed':False,'merge_authority':False,'delete_authority':False})
    return out
