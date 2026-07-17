from __future__ import annotations
import json
from pathlib import Path
from .types import ApprovalRecord,EvidenceRecord,SecurityControlResult,TransitionRequest,WaiverRecord
from .service import EvaluationBundle

def load_json(path:Path): return json.loads(path.read_text(encoding="utf-8"))
def load_bundle(path:Path)->EvaluationBundle:
    obj=load_json(path)
    allowed={"request","evidence","approvals","security_results","waiver"}; unknown=set(obj)-allowed
    if unknown: raise ValueError(f"bundle unknown fields: {sorted(unknown)}")
    return EvaluationBundle(TransitionRequest.from_dict(obj["request"]),tuple(EvidenceRecord.from_dict(x) for x in obj.get("evidence",[])),tuple(ApprovalRecord.from_dict(x) for x in obj.get("approvals",[])),tuple(SecurityControlResult.from_dict(x) for x in obj.get("security_results",[])),WaiverRecord.from_dict(obj["waiver"]) if obj.get("waiver") else None)
