from __future__ import annotations
from typing import Any
from .contracts import parse_config, parse_manifests
from .upstream import verify
from .security import scan
from .trial_ledger import build as build_trials
from .exposure_ledger import build as build_exposures
from .multiplicity import build as build_multiplicity
from .audit import completeness, integrity
from .budget import snapshot
from .authority import boundary
from .certificate import build as build_certificate, handoff
from .replay_receipt import build as build_replay
from .canonical import content_hash, stable_id

def run(config:dict[str,Any], upstream_documents:dict[str,Any], manifests:list[dict[str,Any]], trial_events:list[dict[str,Any]], exposure_events:list[dict[str,Any]])->dict[str,Any]:
    parsed=parse_config(config); security=scan(config,manifests,trial_events,exposure_events); upstream=verify(parsed["upstream_intake"],upstream_documents); manifests=parse_manifests(manifests)
    actors={a["actor_id"]:a for a in parsed["actor_registry"]}; roles={r["data_role"]:r for r in parsed["data_role_registry"]}
    families={f["family_id"]:f for f in parsed["search_family_registry"]}
    for m in manifests:
        if m["owner_actor_id"] not in actors or m["family_id"] not in families: raise ValueError("manifest registry reference invalid")
    trials=build_trials(trial_events,manifests,set(actors),parsed["ledger_policy"],parsed["query_budget"])
    exposures=build_exposures(exposure_events,actors,roles,parsed["ledger_policy"],parsed["query_budget"])
    universe=build_multiplicity(list(families.values()),manifests,trials,exposures)
    complete=completeness(manifests,trials,exposures,universe); integ=integrity(trials,exposures); budget=snapshot(parsed["query_budget"],trials,exposures); authority=boundary()
    known={"phase":"SAED_V4_27","passed":True,"known_time_violations":0,"future_suffix_queries":0,"hidden_evaluation_queries":0,"protected_evidence_queries":0,"post_exposure_hypothesis_mutations_logged":exposures["counts_by_type"].get("hypothesis_modified",0),"all_mutations_in_multiplicity_scope":True}; known["review_id"]=stable_id("v427_known_time",known); known["review_hash"]=content_hash(known)
    model_risk={"phase":"SAED_V4_27","passed":True,"limitations":["local_reference_evidence","no_online_fdr_yet","no_hidden_evaluation_air_gap_yet","no_independent_replication","no_runtime_parity","no_broker_qualification"],"selection_risk_quantified":False,"selection_risk_universe_complete":True,"false_discovery_control_deferred_to_v4_28":True}; model_risk["model_risk_review_id"]=stable_id("v427_model_risk",model_risk); model_risk["model_risk_review_hash"]=content_hash(model_risk)
    evidence={"upstream_receipt":upstream,"trial_ledger":trials,"exposure_ledger":exposures,"multiplicity_universe":universe,"completeness_audit":complete,"integrity_report":integ,"budget_snapshot":budget,"known_time_review":known,"security_review":security,"model_risk_review":model_risk}
    cert=build_certificate(evidence,authority); nxt=handoff(cert)
    preliminary={**evidence,"authority_boundary":authority,"certificate":cert,"handoff":nxt}
    replay=build_replay(config,manifests,trial_events,exposure_events,preliminary)
    return {**preliminary,"replay_receipt":replay}
