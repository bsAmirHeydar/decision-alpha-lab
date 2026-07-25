from __future__ import annotations
from collections import deque
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .expression import evaluate
from .errors import VerificationError

INV_KEYS=["invariant_id","name","expression","severity","rationale"]
TEMP_KEYS=["property_id","name","kind","expression","trigger","target","bound","severity","rationale"]

def freeze_invariants(catalog:list)->dict:
    require_list(catalog,"invariants",1); require_unique(catalog,"invariant_id","invariants")
    for item in catalog: require_exact(item,INV_KEYS,name="invariant")
    body={"phase":"SAED_V4_31","invariants":catalog,"count":len(catalog),"closed":True,"research_only":True}
    body["catalog_id"]=stable_id("v431_invariant_catalog",body); body["catalog_hash"]=content_hash(body); return body

def freeze_temporal(catalog:list)->dict:
    require_list(catalog,"temporal_properties",1); require_unique(catalog,"property_id","temporal_properties")
    for item in catalog:
        require_exact(item,TEMP_KEYS,name="temporal_property")
        if item["kind"] not in {"always","never","reachable","terminal","transition_always","leads_to_within"}: raise VerificationError("unsupported temporal kind")
        if not isinstance(item["bound"],int) or item["bound"]<0: raise VerificationError("invalid bound")
    body={"phase":"SAED_V4_31","properties":catalog,"count":len(catalog),"closed":True,"bounded_semantics":True,"research_only":True}
    body["catalog_id"]=stable_id("v431_temporal_catalog",body); body["catalog_hash"]=content_hash(body); return body

def _adjacency(graph:dict)->dict[str,list[str]]:
    out={x["state_id"]:[] for x in graph["states"]}
    for edge in graph["edges"]: out[edge["source_state_id"]].append(edge["target_state_id"])
    return out

def _can_reach_target(start:str,target_ids:set[str],adj:dict[str,list[str]],bound:int)->bool:
    if start in target_ids: return True
    q=deque([(start,0)]); seen={start}
    while q:
        node,depth=q.popleft()
        if depth>=bound: continue
        for nxt in adj[node]:
            if nxt in target_ids: return True
            if nxt not in seen: seen.add(nxt); q.append((nxt,depth+1))
    return False

def check_invariants(graph:dict,catalog:dict)->dict:
    results=[]
    for invariant in catalog["invariants"]:
        failures=[]
        for state in graph["states"]:
            if not evaluate(invariant["expression"],state["values"]): failures.append({"state_id":state["state_id"],"path":state["shortest_transition_path"],"values":state["values"]})
        results.append({"invariant_id":invariant["invariant_id"],"passed":not failures,"failure_count":len(failures),"counterexamples":failures[:8],"severity":invariant["severity"]})
    body={"phase":"SAED_V4_31","model_id":graph["model_id"],"catalog_id":catalog["catalog_id"],"results":results,"passed":all(x["passed"] for x in results),"checked_state_count":graph["state_count"],"research_only":True}
    body["report_id"]=stable_id("v431_invariant_report",body); body["report_hash"]=content_hash(body); return body

def check_temporal(graph:dict,catalog:dict)->dict:
    states={x["state_id"]:x for x in graph["states"]}; adj=_adjacency(graph); results=[]
    edge_envs=[]
    for edge in graph["edges"]:
        pre=states[edge["source_state_id"]]["values"]; post=states[edge["target_state_id"]]["values"]
        env={f"pre_{k}":v for k,v in pre.items()}|{f"post_{k}":v for k,v in post.items()}|{"action":edge["action"]}
        edge_envs.append((edge,env))
    for prop in catalog["properties"]:
        kind=prop["kind"]; failures=[]
        if kind in {"always","never","reachable","terminal","leads_to_within"}:
            matches=[s for s in graph["states"] if evaluate(prop["expression"] if kind not in {"leads_to_within"} else prop["trigger"],s["values"])]
            if kind=="always": failures=[{"state_id":s["state_id"],"path":s["shortest_transition_path"]} for s in graph["states"] if not evaluate(prop["expression"],s["values"])]
            elif kind=="never": failures=[{"state_id":s["state_id"],"path":s["shortest_transition_path"]} for s in matches]
            elif kind=="reachable" and not matches: failures=[{"reason":"no_reachable_matching_state"}]
            elif kind=="terminal":
                outgoing={e["source_state_id"] for e in graph["edges"]}
                failures=[{"state_id":s["state_id"],"path":s["shortest_transition_path"]} for s in matches if s["state_id"] in outgoing]
            elif kind=="leads_to_within":
                targets={s["state_id"] for s in graph["states"] if evaluate(prop["target"],s["values"])}
                failures=[{"state_id":s["state_id"],"path":s["shortest_transition_path"],"bound":prop["bound"]} for s in matches if not _can_reach_target(s["state_id"],targets,adj,prop["bound"])]
        elif kind=="transition_always":
            failures=[{"transition_id":edge["transition_id"],"source_state_id":edge["source_state_id"],"target_state_id":edge["target_state_id"]} for edge,env in edge_envs if not evaluate(prop["expression"],env)]
        results.append({"property_id":prop["property_id"],"kind":kind,"passed":not failures,"failure_count":len(failures),"counterexamples":failures[:8],"severity":prop["severity"]})
    body={"phase":"SAED_V4_31","model_id":graph["model_id"],"catalog_id":catalog["catalog_id"],"results":results,"passed":all(x["passed"] for x in results),"bounded_semantics":True,"research_only":True}
    body["report_id"]=stable_id("v431_temporal_report",body); body["report_hash"]=content_hash(body); return body
