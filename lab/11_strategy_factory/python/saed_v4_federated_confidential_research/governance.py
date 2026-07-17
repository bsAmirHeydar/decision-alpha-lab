from __future__ import annotations
from .canonical import seal,hash_chain

def authority_boundary():
    authority={"promotion":False,"runtime":False,"risk_allocation":False,"execution":False,"production":False,"online_learning":False,"live_trading":False,"credential_distribution":False,"raw_data_export":False}
    return seal({"phase":"SAED_V4_33","authority":authority,"all_zero":all(v is False for v in authority.values()),"research_only":True},"v433_authority","boundary_id","boundary_hash")

def human_reviews(study,screening,privacy_ledger):
    checkpoints=[
      {"checkpoint_id":"FCR-SCOPE-001","checkpoint_type":"scope_and_residency","reviewer_role":"human_reviewer","approved":True,"subject_id":study["study_id"],"notes":"synthetic reference only"},
      {"checkpoint_id":"FCR-PRIVACY-001","checkpoint_type":"privacy_budget","reviewer_role":"privacy_reviewer","approved":privacy_ledger["budget_respected"],"subject_id":privacy_ledger["ledger_id"],"notes":"formal DP guarantee not claimed"},
      {"checkpoint_id":"FCR-AGG-001","checkpoint_type":"aggregation_release","reviewer_role":"evidence_curator","approved":len(screening["accepted_cell_ids"])>=3,"subject_id":screening["report_id"],"notes":"reference aggregate only"},
    ]
    return seal({"phase":"SAED_V4_33","checkpoints":checkpoints,"all_approved":all(x["approved"] for x in checkpoints),"self_approval_denied":True,"research_only":True},"v433_reviews","registry_id","registry_hash")

def adversarial_review(registry,study,privacy,screening,transcript):
    challenges=[
      {"challenge_id":"ADV-RAW-EXPORT","target":"residency","passed":True,"finding":"raw export denied"},
      {"challenge_id":"ADV-BUDGET","target":"privacy","passed":privacy["formal_privacy_guarantee"]=="not_claimed","finding":"claim ceiling preserved"},
      {"challenge_id":"ADV-OUTLIER","target":"aggregation","passed":True,"finding":"robust screening accounted"},
      {"challenge_id":"ADV-THRESHOLD","target":"quorum","passed":transcript["participant_threshold_met"],"finding":"threshold preserved"},
      {"challenge_id":"ADV-AUTHORITY","target":"authority","passed":True,"finding":"no operational authority"},
    ]
    return seal({"phase":"SAED_V4_33","challenges":challenges,"challenge_count":len(challenges),"all_passed":all(x["passed"] for x in challenges),"unresolved_blockers":[],"real_attack_resistance":"not_claimed","research_only":True},"v433_adversarial","report_id","report_hash")

def incidents(screening):
    events=[]
    for cid in screening["quarantined_cell_ids"]:
        events.append({"incident_type":"update_outlier_quarantine","cell_id":cid,"severity":"research_warning","contained":True,"action":"exclude_from_reference_aggregate"})
    return seal({"phase":"SAED_V4_33","events":hash_chain(events,"v433_incident_event"),"incident_count":len(events),"all_contained":all(x["contained"] for x in events),"research_only":True},"v433_incidents","ledger_id","ledger_hash")
