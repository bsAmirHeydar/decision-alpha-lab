from __future__ import annotations
from collections import Counter
from typing import Any
from .canonical import content_hash, stable_id

def completeness(manifests, trial, exposure, multiplicity):
    expected=sum(len(m["expected_trial_ids"]) for m in manifests)
    checks={"all_manifests_hash_bound":all(bool(m["manifest_hash"] and m["code_hash"] and m["config_hash"] and m["dataset_hash"]) for m in manifests),"expected_trials_equal_observed":expected==trial["observed_trial_count"],"all_trials_terminal":not trial["nonterminal_trial_ids"],"no_orphan_trials":not trial["orphan_trial_ids"],"no_missing_trials":not trial["missing_trial_ids"],"failure_states_accounted":all(k in trial["terminal_state_counts"] for k in ["failed","timed_out","pruned"]),"duplicates_accounted":bool(trial["duplicate_edges"]),"retries_accounted":bool(trial["retry_edges"]),"trial_chain_verified":trial["chain_receipt"]["verified"],"exposure_chain_verified":exposure["chain_receipt"]["verified"],"protected_exposure_zero":exposure["protected_evidence_exposures"]==0,"hidden_query_zero":exposure["hidden_evaluation_queries"]==0,"multiplicity_complete":multiplicity["complete_materially_related_universe"]}
    payload={"phase":"SAED_V4_27","checks":checks,"passed":all(checks.values()),"expected_trials":expected,"observed_trials":trial["observed_trial_count"],"trial_events":trial["event_count"],"exposure_events":exposure["event_count"],"unclassified_failures":0}
    payload["audit_id"]=stable_id("ledger_completeness_audit",payload); payload["audit_hash"]=content_hash(payload)
    return payload

def integrity(trial, exposure):
    checks={"trial_hash_chain":trial["chain_receipt"]["verified"],"exposure_hash_chain":exposure["chain_receipt"]["verified"],"trial_head_present":trial["chain_receipt"]["head_hash"]!="0"*64,"exposure_head_present":exposure["chain_receipt"]["head_hash"]!="0"*64,"append_only_claim":trial["append_only"] and exposure["append_only"],"content_addressed":len(trial["trial_ledger_hash"])==64 and len(exposure["exposure_ledger_hash"])==64}
    payload={"phase":"SAED_V4_27","checks":checks,"passed":all(checks.values()),"trial_chain_head":trial["chain_receipt"]["head_hash"],"exposure_chain_head":exposure["chain_receipt"]["head_hash"],"tamper_evidence":"sha256_hash_linked_append_only_reference"}
    payload["integrity_report_id"]=stable_id("ledger_integrity",payload); payload["integrity_report_hash"]=content_hash(payload)
    return payload
