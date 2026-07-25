from __future__ import annotations
from datetime import datetime
from .canonical import content_hash, stable_id
from .errors import EvidenceError

def _dt(x): return datetime.fromisoformat(x.replace("Z","+00:00"))

def build_registry(hypotheses):
    rows=[]; discarded=0; quarantined=[]
    for h in hypotheses:
        decision=_dt(h["decision_time"]); known=[x for x in h["looks"] if _dt(x["known_at"])<=decision]; future=[x for x in h["looks"] if _dt(x["known_at"])>decision]
        discarded+=len(future)
        if not known:
            quarantined.append(h["hypothesis_id"]); continue
        if any(x["anytime_p_value"]<0 or x["anytime_p_value"]>1 or x["e_value"]<0 for x in known): raise EvidenceError("invalid evidence range")
        chosen=known[-1]
        row={"hypothesis_id":h["hypothesis_id"],"sequence":h["sequence"],"family_id":h["family_id"],"experiment_id":h["experiment_id"],"trial_id":h["trial_id"],"metric_name":h["metric_name"],"truth_label":h["truth_label"],"data_role":h["data_role"],"decision_time":h["decision_time"],"stopping_rule_id":h["stopping_rule_id"],"eligible":bool(h["eligible"]),"known_look_count":len(known),"future_look_count":len(future),"selected_look_sequence":chosen["look_sequence"],"selected_known_at":chosen["known_at"],"anytime_p_value":chosen["anytime_p_value"],"e_value":chosen["e_value"],"statistic":chosen["statistic"],"evidence_hash":chosen["evidence_hash"],"future_suffix_ignored":len(future)>0}
        row["record_hash"]=content_hash(row); rows.append(row)
    payload={"phase":"SAED_V4_28","records":rows,"record_count":len(rows),"quarantined_hypothesis_ids":quarantined,"future_look_count_discarded":discarded,"future_suffix_invariant":True,"anytime_p_process_required":True,"e_process_supported":True,"known_time_enforced":True,"deterministic":True}
    payload["registry_id"]=stable_id("anytime_evidence_registry",payload); payload["registry_hash"]=content_hash(payload); return payload
