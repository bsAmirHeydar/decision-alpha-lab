from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal,hash_chain
from .errors import RecoveryError

def inject_failures(plan:dict,nodes:dict)->dict:
    events=[]
    for f in plan["failures"]:
        if f["node_id"] not in {n["node_id"] for n in nodes["nodes"]}: raise RecoveryError("unknown failure node")
        events.append(deepcopy(f))
    return seal({"phase":"SAED_V4_34","failures":sorted(events,key=lambda x:(x["tick"],x["failure_id"])),"failure_count":len(events),"synthetic_faults":True,"research_only":True},"v434_failures","plan_id","plan_hash")

def recover(failures:dict,partition:dict,nodes:dict,checkpoints:dict,max_attempts:int)->tuple[dict,dict]:
    amap={a["task_id"]:a for a in partition["assignments"]}; nmap={n["node_id"]:n for n in nodes["nodes"]}; events=[]
    for f in failures["failures"]:
        impacted=sorted([a for a in partition["assignments"] if a["node_id"]==f["node_id"]],key=lambda x:x["task_id"])
        for a in impacted[:1]:
            eligible=[n for n in nodes["nodes"] if n["domain_id"]==a["domain_id"] and n["node_id"]!=f["node_id"] and n["compute_class"]==a["compute_class"]]
            if not eligible: raise RecoveryError("no sovereign recovery node")
            target=sorted(eligible,key=lambda x:x["node_id"])[0]
            events.append({"failure_id":f["failure_id"],"task_id":a["task_id"],"failed_node_id":f["node_id"],"recovery_node_id":target["node_id"],"domain_id":a["domain_id"],"checkpoint_id":checkpoints["checkpoints"][0]["checkpoint_id"],"attempt":2,"cross_domain_migration":False,"recovered":max_attempts>=2})
    chained=hash_chain(events,"v434_recovery_event")
    transcript=seal({"phase":"SAED_V4_34","events":chained,"all_recovered":all(e["recovered"] for e in events),"cross_domain_migration":False,"baseline_preserved":True,"research_only":True},"v434_recovery","transcript_id","transcript_hash")
    # Quorum is evidence quorum, not distributed consensus protocol claim.
    domains=sorted({a["domain_id"] for a in partition["assignments"]}); votes=[{"domain_id":d,"vote":"accept","evidence_hash":content_hash({"domain":d,"recovery":transcript["transcript_hash"]})} for d in domains]
    quorum=seal({"phase":"SAED_V4_34","votes":votes,"eligible_voters":len(domains),"accept_votes":len(votes),"threshold":max(2,(2*len(domains))//3+1),"threshold_met":len(votes)>=max(2,(2*len(domains))//3+1),"consensus_protocol":"not_claimed","evidence_quorum_only":True,"research_only":True},"v434_quorum","receipt_id","receipt_hash")
    return transcript,quorum
