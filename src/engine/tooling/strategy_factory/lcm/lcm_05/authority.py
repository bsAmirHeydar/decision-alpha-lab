from datetime import datetime,timedelta,timezone
from .canonical import content_id,digest_object
from .errors import PolicyError
ACTION="LCM05_DEFINE_TARGET_TOPOLOGY"
def build_permit(handoff_digest,characterization_run_id,issued_at):
    dt=datetime.fromisoformat(issued_at.replace("Z","+00:00"));exp=(dt+timedelta(days=7)).astimezone(timezone.utc).isoformat().replace("+00:00","Z")
    obj={"schema_version":"1.0.0","phase_id":"LCM-05","action":ACTION,"permit_id":content_id("PERMIT",[handoff_digest,characterization_run_id,issued_at]),"source_handoff_digest":handoff_digest,"characterization_run_id":characterization_run_id,"issuer":"ALPHA_LAB_MIGRATION_CONTROL_PLANE","issued_at":issued_at,"expires_at":exp,"source_move_allowed":False,"source_delete_allowed":False,"target_materialization_allowed":False,"semantic_refactor_allowed":False,"merge_allowed":False,"runtime_authority":False,"live_order_authority":False,"capital_authority":False,"permit_digest":None};obj["permit_digest"]=digest_object(obj,"permit_digest");return obj
def verify_permit(p,expected):
    if p.get("action")!=ACTION or p.get("source_handoff_digest")!=expected:raise PolicyError("permit binding invalid")
    for k in ["source_move_allowed","source_delete_allowed","target_materialization_allowed","semantic_refactor_allowed","merge_allowed","runtime_authority","live_order_authority","capital_authority"]:
        if p.get(k) is not False:raise PolicyError(f"authority escalation: {k}")
    if digest_object(p,"permit_digest")!=p.get("permit_digest"):raise PolicyError("permit digest invalid")
    return True
