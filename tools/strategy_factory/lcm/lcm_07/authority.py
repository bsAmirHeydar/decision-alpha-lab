from datetime import datetime,timezone,timedelta
from .canonical import content_id,digest_object
from .constants import PHASE_ID,ACTION,ALLOWED_ACTIONS,FORBIDDEN_ACTIONS,DENIAL_FIELDS
from .errors import PolicyError

def _ts(v):
    try:x=datetime.fromisoformat(v.replace("Z","+00:00"))
    except Exception as e: raise PolicyError("invalid timestamp") from e
    if x.tzinfo is None: raise PolicyError("naive timestamp forbidden")
    return x.astimezone(timezone.utc)
def build_permit(handoff_digest,framework_run_id,issued_at):
    issued=_ts(issued_at); expires=(issued+timedelta(days=7)).isoformat().replace("+00:00","Z")
    o={"schema_version":"1.0.0","phase_id":PHASE_ID,"action":ACTION,"permit_id":content_id("PERMIT",[handoff_digest,framework_run_id,issued_at]),"source_handoff_digest":handoff_digest,"framework_run_id":framework_run_id,"issuer":"ALPHA_LAB_MIGRATION_CONTROL_PLANE","issued_at":issued_at,"expires_at":expires,"allowed_actions":list(ALLOWED_ACTIONS),"forbidden_actions":list(FORBIDDEN_ACTIONS),"shared_engine_extraction_authorized":False,**{k:False for k in DENIAL_FIELDS},"permit_digest":None};o["permit_digest"]=digest_object(o,"permit_digest");return o
def verify_permit(o,expected_handoff,expected_framework):
    if o.get("phase_id")!=PHASE_ID or o.get("action")!=ACTION or o.get("source_handoff_digest")!=expected_handoff or o.get("framework_run_id")!=expected_framework: raise PolicyError("permit binding invalid")
    if _ts(o["expires_at"])<=_ts(o["issued_at"]): raise PolicyError("permit expiry invalid")
    if o.get("permit_id")!=content_id("PERMIT",[o["source_handoff_digest"],o["framework_run_id"],o["issued_at"]]): raise PolicyError("permit identity invalid")
    if o.get("shared_engine_extraction_authorized") is not False: raise PolicyError("extraction authority escalation")
    if any(o.get(k) is not False for k in DENIAL_FIELDS): raise PolicyError("migration authority escalation")
    if tuple(o.get("allowed_actions",[]))!=ALLOWED_ACTIONS or tuple(o.get("forbidden_actions",[]))!=FORBIDDEN_ACTIONS: raise PolicyError("permit action registry drift")
    if digest_object(o,"permit_digest")!=o.get("permit_digest"): raise PolicyError("permit digest invalid")
    return True
