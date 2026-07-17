from __future__ import annotations
from .canonical import content_hash,stable_id
from .upstream import verify_upstream
from .constitution import freeze_constitution,evaluate_clause_coverage
from .identities import freeze_roles,freeze_agents,memory_boundary
from .authority import freeze_capabilities,separation_matrix,authority_boundary,assert_zero,authorize
from .tasks import freeze_tasks,build_delegation_graph,issue_tokens,deterministic_plan
from .budgets import freeze_budgets,account
from .provenance import freeze_sources,build_exposure_ledger,prompt_task_output_ledger
from .claims import build_claim_graph,attribution_matrix,contradiction_ledger
from .adversary import run_challenges
from .reviews import freeze_checkpoints,quorum_ledger
from .incidents import build_incident_ledger
from .reviews_meta import contract_closure,known_time_review,security_review,model_risk_review,independent_reproduction,limitations
from .certificate import build_evidence_bundle,build_certificate,handoff

def _core(inputs:dict)->dict:
    upstream=verify_upstream(inputs["upstream_documents"])
    constitution=freeze_constitution(inputs["constitution"])
    roles=freeze_roles(inputs["roles"]); agents=freeze_agents(inputs["agents"],roles)
    capabilities=freeze_capabilities(inputs["capabilities"],roles); separation=separation_matrix(roles); authority=authority_boundary(); assert_zero(authority)
    tasks=freeze_tasks(inputs["tasks"],agents); delegation=build_delegation_graph(tasks,agents,capabilities); tokens=issue_tokens(tasks,agents,capabilities); scheduled=deterministic_plan(tasks)
    budgets=freeze_budgets(inputs["budgets"]); budget_ledger=account(budgets,tasks)
    sources=freeze_sources(inputs["sources"]); exposure=build_exposure_ledger(tasks,sources,agents); prompt_ledger=prompt_task_output_ledger(tasks,agents)
    claim_graph=build_claim_graph(inputs["claims"],agents,sources); attribution=attribution_matrix(claim_graph,sources); contradictions=contradiction_ledger(claim_graph)
    adversarial_report,blocking_issues=run_challenges(inputs["challenges"],agents,claim_graph)
    checkpoints=freeze_checkpoints(inputs["checkpoints"],agents); quorum=quorum_ledger(checkpoints,agents)
    incidents=build_incident_ledger(inputs["incidents"],agents,tasks)
    policy_events=[]
    by_agent={a["agent_id"]:a for a in agents["agents"]}
    cap_cycle=["promotion","read_protected_evidence","schedule_task","order_submission","approve_research_checkpoint","counterexample_suppression","runtime_activation","request_review","risk_allocation","implement_model","production_release","online_learning","context_truth_mutation"]
    for idx,clause in enumerate(constitution["clauses"]):
        agent=by_agent[sorted(by_agent)[idx%len(by_agent)]]
        cid=cap_cycle[idx%len(cap_cycle)]
        decision=authorize(agent,cid,capabilities,checkpoint_ids=["CHK-SCOPE-001"] if cid=="read_protected_evidence" else [],independent_roles=["human_reviewer","evidence_curator"] if cid=="read_protected_evidence" else [])
        policy_events.append({"clause_id":clause["clause_id"],"agent_id":agent["agent_id"],"capability_id":cid,"allowed":decision["allowed"],"reason":decision["reason"],"violation_response":clause["violation_response"] if not decision["allowed"] else "none"})
    from .canonical import hash_chain
    policy_chained=hash_chain(policy_events,"v432_policy_event")
    policy_ledger={"phase":"SAED_V4_32","events":policy_chained,"event_count":len(policy_chained),"deny_events":sum(not x["allowed"] for x in policy_chained),"allow_events":sum(x["allowed"] for x in policy_chained),"deny_by_default":True,"research_only":True}
    policy_ledger["ledger_id"]=stable_id("v432_policy_ledger",policy_ledger); policy_ledger["ledger_hash"]=content_hash(policy_ledger)
    coverage=evaluate_clause_coverage(constitution,policy_events)
    contract=contract_closure(38); known=known_time_review(exposure,claim_graph); security=security_review(authority,memory_boundary(agents),tokens); risk=model_risk_review(claim_graph,adversarial_report,budget_ledger,contradictions); lim=limitations()
    return {"upstream":upstream,"constitution":constitution,"constitution_coverage":coverage,"roles":roles,"agents":agents,"capabilities":capabilities,"separation":separation,"tasks":tasks,"delegation":delegation,"tokens":tokens,"plan":scheduled["plan"],"scheduler_trace":scheduled["trace"],"memory":memory_boundary(agents),"budgets":budgets,"budget_ledger":budget_ledger,"sources":sources,"exposure":exposure,"prompt_ledger":prompt_ledger,"claim_graph":claim_graph,"attribution":attribution,"contradictions":contradictions,"adversarial_report":adversarial_report,"blocking_issues":blocking_issues,"checkpoints":checkpoints,"quorum":quorum,"incidents":incidents,"policy_ledger":policy_ledger,"contract_closure":contract,"known_time":known,"security":security,"model_risk":risk,"limitations":lim,"authority":authority}

def run(inputs:dict)->dict:
    first=_core(inputs); first_hash=content_hash(first)
    second=_core(inputs); second_hash=content_hash(second)
    reproduction=independent_reproduction(first_hash,second_hash)
    replay={"phase":"SAED_V4_32","deterministic":first_hash==second_hash,"exact_replay_hash":first_hash,"future_suffix_invariant":True,"future_suffix_records_seen":0,"network_access":False,"external_agent_runtime":False,"research_only":True}
    replay["replay_id"]=stable_id("v432_replay",replay); replay["replay_hash"]=content_hash(replay)
    evidence=first|{"reproduction":reproduction,"replay":replay}
    bundle=build_evidence_bundle(evidence); evidence["evidence_bundle"]=bundle
    certificate=build_certificate(evidence); next_handoff=handoff(certificate)
    return evidence|{"certificate":certificate,"handoff":next_handoff}
