from __future__ import annotations
from copy import deepcopy
from collections import deque
from .canonical import content_hash,seal,q,dec
from .contracts import require_exact,require_list,require_unique,require_num,require_time_before
from .errors import FXError

def freeze_fx_snapshot(base_currency:str,rates:list[dict],cutoff:str)->dict:
    rates=require_list(rates,"fx_rates",2); require_unique(rates,"rate_id","fx_rates"); out=[]
    for x in rates:
        require_exact(x,["rate_id","base","quote","mid","spread_bps","known_time","synthetic_fixture"]); require_num(x["mid"],"mid",0.00000001); require_num(x["spread_bps"],"spread_bps",0); require_time_before(x["known_time"],cutoff,"fx.known_time")
        y=deepcopy(x); y["rate_hash"]=content_hash(y); out.append(y)
    return seal({"phase":"SAED_V4_37","base_currency":base_currency,"cutoff_time":cutoff,"rates":sorted(out,key=lambda x:x["rate_id"]),"research_only":True},"v437_fx","snapshot_id","snapshot_hash")

def conversion_rate(snapshot:dict,source:str,target:str)->float:
    if source==target:return 1.0
    g={}
    for r in snapshot["rates"]:
        g.setdefault(r["base"],[]).append((r["quote"],float(r["mid"])))
        g.setdefault(r["quote"],[]).append((r["base"],1.0/float(r["mid"])))
    queue=deque([(source,1.0)]); seen={source}
    while queue:
        c,v=queue.popleft()
        for nxt,m in sorted(g.get(c,[])):
            if nxt==target:return float(q(dec(v)*dec(m)))
            if nxt not in seen: seen.add(nxt); queue.append((nxt,v*m))
    raise FXError(f"no FX path {source}->{target}")

def convert(snapshot:dict,amount:float,source:str,target:str)->float:return float(q(dec(amount)*dec(conversion_rate(snapshot,source,target))))
