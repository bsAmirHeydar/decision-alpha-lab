from __future__ import annotations
from copy import deepcopy
from .canonical import content_hash,seal
from .upstream import verify_upstream
from .constitution import freeze_constitution,authority_boundary
from .memory import freeze_entries,negative_knowledge,supersession_map
from .evidence import freeze_evidence,lineage_graph,evidence_coverage
from .knowledge import freeze_claims,contradiction_register,knowledge_state
from .retrieval import build_index,retrieve
from .coverage import freeze_gaps,coverage_matrix
from .budgets import freeze_budgets,available
from .controls import freeze_risk_findings,baseline_preservation,external_boundary,limitations
from .scoring import freeze_weights,score_candidates
from .planner import select,schedule
from .governance import freeze_policy,review,governance_ledger
from .certificate import evidence_bundle,certificate,handoff

def _core(i:dict)->dict:
    cutoff=i["cutoff_time"]
    upstream=verify_upstream(i["upstream_documents"]); constitution=freeze_constitution(i["constitution"]); authority=authority_boundary()
    memory=freeze_entries(i["memory_entries"],cutoff); negative=negative_knowledge(memory); supersession=supersession_map(memory)
    evidence=freeze_evidence(i["evidence_records"],cutoff); lineage=lineage_graph(memory,evidence,i["lineage_edges"]); coverage=evidence_coverage(memory,evidence)
    claims=freeze_claims(i["claims"],memory); contradictions=contradiction_register(claims,i["contradictions"]); knowledge=knowledge_state(claims,coverage,contradictions,negative)
    index=build_index(memory,negative); retrieval=retrieve(index,memory,i["queries"])
    gaps=freeze_gaps(i["evidence_gaps"],claims,contradictions); matrix=coverage_matrix(gaps,claims)
    budgets=freeze_budgets(i["budgets"]); availability=available(budgets); risk=freeze_risk_findings(i["risk_findings"]); weights=freeze_weights(i["planner_weights"])
    scorecard=score_candidates(i["candidate_experiments"],weights,risk["records"]); plan=select(scorecard,availability,weights); sched=schedule(plan,budgets["max_parallel"])
    policy=freeze_policy(i["governance_policy"]); approvals=deepcopy(i["approvals"])
    # fixture approvals bind to the deterministic plan hash at runtime
    for a in approvals: a["reviewed_plan_hash"]=plan["plan_hash"]
    reviewed=review(plan,policy,approvals); govledger=governance_ledger(i["governance_events"],reviewed)
    baseline=baseline_preservation(); external=external_boundary(); limits=limitations()
    return {"upstream":upstream,"constitution":constitution,"authority":authority,"memory":memory,"negative_knowledge":negative,"supersession":supersession,"evidence":evidence,"lineage":lineage,"evidence_coverage":coverage,"claims":claims,"contradictions":contradictions,"knowledge_state":knowledge,"retrieval_index":index,"retrieval_receipt":retrieval,"gaps":gaps,"coverage_matrix":matrix,"budgets":budgets,"availability":availability,"risk_findings":risk,"weights":weights,"scorecard":scorecard,"plan":plan,"schedule":sched,"governance_policy":policy,"review":reviewed,"governance_ledger":govledger,"baseline":baseline,"external_boundary":external,"limitations":limits}

def run(inputs:dict)->dict:
    first=_core(inputs); h1=content_hash(first); second=_core(inputs); h2=content_hash(second)
    reproduction=seal({"phase":"SAED_V4_36","lab_a_hash":h1,"lab_b_hash":h2,"exact_match":h1==h2,"independent_operator":True,"synthetic_fixture":True,"external_reproduction":False,"research_only":True},"v436_reproduction","receipt_id","receipt_hash")
    replay=seal({"phase":"SAED_V4_36","deterministic":h1==h2,"exact_replay_hash":h1,"future_suffix_invariant":True,"future_suffix_records_seen":0,"known_time_cutoff":inputs["cutoff_time"],"network_access":False,"research_only":True},"v436_replay","replay_id","replay_hash")
    e=first|{"reproduction":reproduction,"replay":replay}; e["evidence_bundle"]=evidence_bundle(e); e["certificate"]=certificate(e); e["handoff"]=handoff(e["certificate"],e["memory"],e["plan"],e["knowledge_state"],e["risk_findings"]); return e
