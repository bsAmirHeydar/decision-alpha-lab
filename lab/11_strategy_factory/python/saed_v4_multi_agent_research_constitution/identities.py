from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,stable_id
from .contracts import require_exact,require_list,require_unique,require_enum,require_bool
from .errors import IdentityError

AGENT_KEYS=["agent_id","display_name","role_id","identity_provider","identity_fingerprint","memory_namespace","prompt_profile_hash","tool_profile_hash","active","human_supervisor_id"]
ROLE_KEYS=["role_id","purpose","independence_group","may_propose","may_review","may_block","may_approve_research","may_access_protected_evidence","may_delegate","research_only"]
ROLE_SET={"orchestrator","hypothesis","data_audit","leakage_sentinel","statistical_adversary","model_engineering","causal_auditor","execution_auditor","evidence_curator","human_reviewer"}

def freeze_roles(roles:list[dict])->dict:
    require_list(roles,"roles",len(ROLE_SET)); require_unique(roles,"role_id","roles")
    normalized=[]
    for r in roles:
        require_exact(r,ROLE_KEYS,name="role")
        require_enum(r["role_id"],ROLE_SET,"role_id")
        require_bool(r["research_only"],"research_only",True)
        if r["may_approve_research"] and r["role_id"]!="human_reviewer": raise IdentityError("only human reviewer may approve research checkpoint")
        if r["may_access_protected_evidence"] and r["role_id"] not in {"human_reviewer","evidence_curator"}: raise IdentityError("protected evidence access too broad")
        normalized.append(deepcopy(r))
    if {r["role_id"] for r in roles}!=ROLE_SET: raise IdentityError("role registry incomplete")
    body={"phase":"SAED_V4_32","roles":sorted(normalized,key=lambda x:x["role_id"]),"deny_by_default":True,"research_only":True}
    body["registry_id"]=stable_id("v432_role_registry",body); body["registry_hash"]=content_hash(body); return body

def freeze_agents(agents:list[dict],roles:dict)->dict:
    require_list(agents,"agents",len(ROLE_SET)); require_unique(agents,"agent_id","agents")
    role_ids={r["role_id"] for r in roles["roles"]}; namespaces=set(); fingerprints=set(); normalized=[]
    for a in agents:
        require_exact(a,AGENT_KEYS,name="agent")
        if a["role_id"] not in role_ids: raise IdentityError("unknown role")
        if a["memory_namespace"] in namespaces: raise IdentityError("memory namespace collision")
        if a["identity_fingerprint"] in fingerprints: raise IdentityError("identity fingerprint collision")
        if a["active"] is not True: raise IdentityError("reference agents must be active")
        if not a["human_supervisor_id"].startswith("human:"): raise IdentityError("human supervisor required")
        namespaces.add(a["memory_namespace"]); fingerprints.add(a["identity_fingerprint"]); normalized.append(deepcopy(a))
    role_counts={rid:sum(a["role_id"]==rid for a in normalized) for rid in sorted(role_ids)}
    if any(v<1 for v in role_counts.values()): raise IdentityError("every role requires an identity")
    body={"phase":"SAED_V4_32","agents":sorted(normalized,key=lambda x:x["agent_id"]),"role_counts":role_counts,"identity_isolation":True,"memory_isolation":True,"research_only":True}
    body["registry_id"]=stable_id("v432_agent_registry",body); body["registry_hash"]=content_hash(body); return body

def memory_boundary(agents:dict)->dict:
    rows=[]
    for a in agents["agents"]:
        rows.append({"agent_id":a["agent_id"],"memory_namespace":a["memory_namespace"],"readable_namespaces":[a["memory_namespace"]],"writable_namespaces":[a["memory_namespace"]],"cross_agent_write":False,"protected_memory_access":a["role_id"] in {"evidence_curator","human_reviewer"}})
    body={"phase":"SAED_V4_32","rows":rows,"namespace_unique":len({r["memory_namespace"] for r in rows})==len(rows),"cross_agent_write_denied":True,"research_only":True}
    body["boundary_id"]=stable_id("v432_memory_boundary",body); body["boundary_hash"]=content_hash(body); return body
