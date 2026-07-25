from __future__ import annotations
from .canonical import content_hash,stable_id

def build_v4_21_handoff(certificate,registry_hash,exposure_hash,qa):
    body={'phase':'SAED_V4_20','next_phase':'SAED_V4_21','selection_certificate_hash':certificate['certificate_hash'],'selection_registry_hash':registry_hash,'exposure_ledger_hash':exposure_hash,'entry_gates':{'closed_contracts':True,'deterministic_replay':True,'baseline_preserved':True,'set_valued_selection':True,'pareto_frontier':True,'abstention_fail_closed':True,'zero_protected_evidence_exposure':True,'zero_hidden_evaluation_queries':True,'research_only':True},'authority':{'select_live_treatment':False,'allocate_risk':False,'sign_promotion':False,'compile_runtime':False,'activate_runtime':False,'send_order':False},'qa':qa,'research_only':True}
    body['handoff_id']=stable_id('v420_to_v421',body);body['handoff_hash']=content_hash(body);return body
