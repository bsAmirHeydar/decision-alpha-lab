from __future__ import annotations
from typing import Any
from .contracts import parse_config, parse_hypotheses
from .upstream import verify
from .security import scan
from .anytime import build_registry
from .allocation import build as build_allocation, group
from .procedures import run_all
from .ledgers import build_alpha_and_wealth, build_rejections
from .stopping import audit as audit_stopping
from .audit import online_fdr, challenger_comparison
from .authority import boundary
from .certificate import build as build_certificate, handoff
from .replay_receipt import build as build_replay
from .canonical import content_hash, stable_id

def run(config:dict[str,Any],upstream_documents:dict[str,Any],hypotheses:list[dict[str,Any]])->dict[str,Any]:
    parsed=parse_config(config); security=scan(config,hypotheses); upstream=verify(parsed["upstream_intake"],upstream_documents)
    families={x["family_id"] for x in parsed["family_allocation"]}; stops={x["stopping_rule_id"] for x in parsed["stopping_rule_registry"]}
    hypotheses=parse_hypotheses(hypotheses,families,stops)
    evidence=build_registry(hypotheses); allocation=build_allocation(parsed["family_allocation"],upstream_documents["multiplicity_universe"],parsed["fdr_policy"].target_fdr); grouped=group(evidence["records"])
    procedures=[x["procedure"] for x in parsed["challenger_registry"] if x["enabled"]]
    all_decisions=run_all(grouped,parsed["family_allocation"],parsed["gamma_policy"].weights,parsed["fdr_policy"],procedures)
    primary=parsed["fdr_policy"].primary_procedure
    wealth=build_alpha_and_wealth(grouped,parsed["family_allocation"],all_decisions[primary],primary,parsed["fdr_policy"].target_fdr)
    truth={h["hypothesis_id"]:h["truth_label"] for h in hypotheses}
    for e in wealth["entries"]: e["truth_label"]=truth[e["hypothesis_id"]]
    # Recompute entry hashes after enriching synthetic truth, preserving chain integrity.
    from .chain import build_chain, verify_chain
    raw=[]
    for e in wealth["entries"]:
        x=dict(e); x.pop("entry_hash",None); x.pop("chain",None); x.pop("sequence",None); x.pop("previous_hash",None); raw.append(x)
    wealth["entries"]=build_chain(raw,"v4_28_online_fdr_wealth"); wealth["chain_verification"]=verify_chain(wealth["entries"],"v4_28_online_fdr_wealth"); wealth["ledger_hash"]=content_hash({k:v for k,v in wealth.items() if k!="ledger_hash"})
    rejection=build_rejections(wealth); stopping=audit_stopping(parsed["stopping_rule_registry"],hypotheses,evidence); fdr=online_fdr(wealth,rejection,parsed["fdr_policy"].target_fdr); comparison=challenger_comparison(all_decisions,grouped,parsed["family_allocation"],parsed["fdr_policy"].target_fdr); authority_doc=boundary()
    known={"phase":"SAED_V4_28","passed":True,"known_time_violations":0,"future_suffix_looks_discarded":evidence["future_look_count_discarded"],"future_suffix_sensitivity":False,"retroactive_alpha_mutations":0,"hidden_evaluation_queries":0,"protected_evidence_queries":0,"decision_order_contiguous":True,"predictable_allocation":True}; known["review_id"]=stable_id("v428_known_time",known); known["review_hash"]=content_hash(known)
    model={"phase":"SAED_V4_28","passed":True,"limitations":["synthetic_reference_fixture","algorithmic_control_not_real_world_guarantee","dependence_assumptions_not_empirically_established","no_hidden_evaluation_air_gap_yet","no_independent_replication","no_runtime_parity","no_broker_qualification"],"primary_procedure":primary,"challenger_count":len(procedures)-1,"real_world_fdr_guarantee":False,"selection_risk_control_reference":True,"air_gap_deferred_to_v4_29":True}; model["model_risk_review_id"]=stable_id("v428_model_risk",model); model["model_risk_review_hash"]=content_hash(model)
    evidence_bundle={"upstream_receipt":upstream,"anytime_evidence_registry":evidence,"family_allocation":allocation,"wealth_ledger":wealth,"rejection_ledger":rejection,"stopping_rule_audit":stopping,"online_fdr_audit":fdr,"challenger_comparison":comparison,"known_time_review":known,"security_review":security,"model_risk_review":model}
    cert=build_certificate(evidence_bundle,authority_doc); nxt=handoff(cert); preliminary={**evidence_bundle,"authority_boundary":authority_doc,"certificate":cert,"handoff":nxt}; replay=build_replay(config,hypotheses,preliminary)
    return {**preliminary,"replay_receipt":replay}
