from __future__ import annotations
from collections import defaultdict,deque
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_enum
from .errors import ProvenanceError

CLAIM_KEYS=["claim_id","claim_class","statement","producer_agent_id","supporting_source_ids","opposing_claim_ids","depends_on_claim_ids","uncertainty_state","decision_contribution","known_time_epoch","status","research_only"]
CLASSES={"descriptive","associational","predictive","causal_hypothesis","stress_only","operational_research"}
UNCERTAINTY={"bounded","material","high","unresolved"}
STATUSES={"proposed","supported_synthetic","challenged","blocked","abstained"}
DECISIONS={"none","skip","abstain","manual_fallback","research_recommendation"}

def build_claim_graph(items:list[dict],agents:dict,sources:dict)->dict:
    require_list(items,"claims",1); require_unique(items,"claim_id","claims")
    agent_ids={a["agent_id"] for a in agents["agents"]}; source_by={s["source_id"]:s for s in sources["sources"]}; ids={c["claim_id"] for c in items}; normalized=[]
    for c in items:
        require_exact(c,CLAIM_KEYS,name="claim")
        require_enum(c["claim_class"],CLASSES,"claim_class"); require_enum(c["uncertainty_state"],UNCERTAINTY,"uncertainty_state"); require_enum(c["status"],STATUSES,"status"); require_enum(c["decision_contribution"],DECISIONS,"decision_contribution")
        if c["producer_agent_id"] not in agent_ids: raise ProvenanceError("unknown claim producer")
        if set(c["supporting_source_ids"])-set(source_by): raise ProvenanceError("unknown supporting source")
        if set(c["opposing_claim_ids"]+c["depends_on_claim_ids"])-ids: raise ProvenanceError("unknown claim edge")
        if c["claim_id"] in c["opposing_claim_ids"]+c["depends_on_claim_ids"]: raise ProvenanceError("self claim edge")
        if any(source_by[s]["known_time_epoch"]>c["known_time_epoch"] for s in c["supporting_source_ids"]): raise ProvenanceError("future source in claim")
        if c["research_only"] is not True: raise ProvenanceError("research_only required")
        normalized.append(deepcopy(c))
    _assert_acyclic(normalized)
    nodes=[]; edges=[]
    for c in sorted(normalized,key=lambda x:x["claim_id"]):
        node=deepcopy(c); node["claim_hash"]=content_hash(c); nodes.append(node)
        for dep in c["depends_on_claim_ids"]: edges.append({"source_claim_id":dep,"target_claim_id":c["claim_id"],"relation":"depends_on"})
        for opp in c["opposing_claim_ids"]: edges.append({"source_claim_id":opp,"target_claim_id":c["claim_id"],"relation":"opposes"})
    body={"phase":"SAED_V4_32","nodes":nodes,"edges":sorted(edges,key=lambda x:(x["target_claim_id"],x["relation"],x["source_claim_id"])),"acyclic_dependency_graph":True,"claim_count":len(nodes),"research_only":True}
    body["graph_id"]=stable_id("v432_claim_graph",body); body["graph_hash"]=content_hash(body); return body

def _assert_acyclic(claims:list[dict])->None:
    ids={c["claim_id"] for c in claims}; indeg={i:0 for i in ids}; children=defaultdict(list)
    for c in claims:
        for dep in c["depends_on_claim_ids"]: indeg[c["claim_id"]]+=1; children[dep].append(c["claim_id"])
    q=deque(sorted(k for k,v in indeg.items() if v==0)); seen=[]
    while q:
        x=q.popleft(); seen.append(x)
        for y in sorted(children[x]):
            indeg[y]-=1
            if indeg[y]==0:q.append(y)
    if len(seen)!=len(ids): raise ProvenanceError("claim dependency cycle")

def attribution_matrix(graph:dict,sources:dict)->dict:
    source_by={s["source_id"]:s for s in sources["sources"]}; rows=[]
    for c in graph["nodes"]:
        for sid in c["supporting_source_ids"]:
            s=source_by[sid]
            rows.append({"claim_id":c["claim_id"],"source_id":sid,"source_hash":s["content_hash"],"evidence_role":s["evidence_role"],"known_time_epoch":s["known_time_epoch"],"protected":s["protected"],"synthetic":s["synthetic"],"attribution_complete":True})
    body={"phase":"SAED_V4_32","rows":sorted(rows,key=lambda x:(x["claim_id"],x["source_id"])),"claim_count":graph["claim_count"],"attributed_claim_count":len({x["claim_id"] for x in rows}),"all_claims_attributed":all(c["supporting_source_ids"] for c in graph["nodes"]),"research_only":True}
    body["matrix_id"]=stable_id("v432_attribution_matrix",body); body["matrix_hash"]=content_hash(body); return body

def contradiction_ledger(graph:dict)->dict:
    pairs=set(); rows=[]
    by={x["claim_id"]:x for x in graph["nodes"]}
    for edge in graph["edges"]:
        if edge["relation"]!="opposes": continue
        pair=tuple(sorted([edge["source_claim_id"],edge["target_claim_id"]]))
        if pair in pairs: continue
        pairs.add(pair); left,right=by[pair[0]],by[pair[1]]
        resolution="block_and_human_review" if left["status"]=="blocked" or right["status"]=="blocked" else "preserve_dissent"
        rows.append({"left_claim_id":pair[0],"right_claim_id":pair[1],"left_status":left["status"],"right_status":right["status"],"resolution":resolution,"suppressed":False,"requires_human_review":True})
    body={"phase":"SAED_V4_32","rows":rows,"contradiction_count":len(rows),"suppressed_count":0,"dissent_preserved":True,"research_only":True}
    body["ledger_id"]=stable_id("v432_contradiction_ledger",body); body["ledger_hash"]=content_hash(body); return body
