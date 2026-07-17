from __future__ import annotations
from collections import defaultdict,deque
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique
from .errors import SafetyCaseError

NODE_KEYS=["node_id","node_type","statement","status","evidence_keys"]
EDGE_KEYS=["source","target","relation"]

def build(plan:dict,evidence:dict)->tuple[dict,dict,dict]:
    require_exact(plan,["root_goal_id","nodes","edges"],name="assurance_case_plan")
    nodes=require_list(plan["nodes"],"nodes",1); edges=require_list(plan["edges"],"edges",1); require_unique(nodes,"node_id","nodes")
    for node in nodes: require_exact(node,NODE_KEYS,name="assurance_node")
    for edge in edges:
        require_exact(edge,EDGE_KEYS,name="assurance_edge")
        if edge["relation"] not in {"supported_by","in_context_of","solved_by","justified_by","assumed_by"}: raise SafetyCaseError("invalid GSN relation")
    node_ids={x["node_id"] for x in nodes}
    if plan["root_goal_id"] not in node_ids: raise SafetyCaseError("missing root goal")
    for edge in edges:
        if edge["source"] not in node_ids or edge["target"] not in node_ids: raise SafetyCaseError("edge references unknown node")
    outgoing=defaultdict(list); indegree={x:0 for x in node_ids}
    for edge in edges: outgoing[edge["source"]].append(edge["target"]); indegree[edge["target"]]+=1
    q=deque([x for x,d in indegree.items() if d==0]); visited=[]
    while q:
        n=q.popleft(); visited.append(n)
        for target in outgoing[n]:
            indegree[target]-=1
            if indegree[target]==0:q.append(target)
    acyclic=len(visited)==len(node_ids)
    reachable=set(); q=deque([plan["root_goal_id"]])
    while q:
        n=q.popleft()
        if n in reachable: continue
        reachable.add(n); q.extend(outgoing[n])
    evidence_hashes={k:content_hash(v) for k,v in evidence.items()}
    resolved=[]
    for node in nodes:
        missing=[key for key in node["evidence_keys"] if key not in evidence_hashes]
        supported=(node["node_type"] not in {"goal","strategy"}) or bool(outgoing[node["node_id"]])
        status="satisfied" if not missing and supported and node["status"]=="active" else "unsatisfied"
        resolved.append({**node,"resolved_status":status,"missing_evidence_keys":missing,"evidence_hashes":{k:evidence_hashes[k] for k in node["evidence_keys"] if k in evidence_hashes}})
    valid=acyclic and reachable==node_ids and all(x["resolved_status"]=="satisfied" for x in resolved)
    graph={"phase":"SAED_V4_31","notation":"GSN_compatible_closed_graph","root_goal_id":plan["root_goal_id"],"nodes":resolved,"edges":edges,"node_count":len(nodes),"edge_count":len(edges),"acyclic":acyclic,"all_nodes_reachable":reachable==node_ids,"valid":valid,"research_only":True}
    graph["graph_id"]=stable_id("v431_assurance_case",graph); graph["graph_hash"]=content_hash(graph)
    claims={"phase":"SAED_V4_31","claims":[{"claim_id":x["node_id"],"statement":x["statement"],"claim_type":x["node_type"],"satisfied":x["resolved_status"]=="satisfied","evidence_hashes":x["evidence_hashes"]} for x in resolved if x["node_type"] in {"goal","strategy"}],"root_claim_id":plan["root_goal_id"],"all_claims_satisfied":valid,"research_only":True}
    claims["ledger_id"]=stable_id("v431_claim_ledger",claims); claims["ledger_hash"]=content_hash(claims)
    trace_rows=[]
    for node in resolved:
        for key,digest in node["evidence_hashes"].items(): trace_rows.append({"node_id":node["node_id"],"evidence_key":key,"evidence_hash":digest,"bound":True})
    trace={"phase":"SAED_V4_31","rows":trace_rows,"row_count":len(trace_rows),"complete":valid and all(x["evidence_keys"]==list(x["evidence_hashes"]) for x in resolved),"research_only":True}
    trace["matrix_id"]=stable_id("v431_traceability",trace); trace["matrix_hash"]=content_hash(trace)
    return graph,claims,trace
