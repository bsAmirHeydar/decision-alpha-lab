from __future__ import annotations
from typing import Any
from .canonical import digest_object
from .errors import ReplayError

def checkpoint(state:dict[str,Any])->dict[str,Any]:
    body={"schema_version":"1.0.0","setup_id":state["setup_id"],"occurrence_id":state["occurrence_id"],"last_sequence":int(state["last_sequence"]),"decision_state":state["decision_state"],"last_decision_digest":state["last_decision_digest"],"reason_codes":list(state.get("reason_codes",[]))}
    return {**body,"checkpoint_digest":digest_object(body)}
def restore(doc:dict[str,Any])->dict[str,Any]:
    if digest_object(doc,"checkpoint_digest")!=doc.get("checkpoint_digest"):raise ReplayError("LCM09B_CHECKPOINT_DIGEST_MISMATCH")
    if int(doc["last_sequence"])<0:raise ReplayError("LCM09B_CHECKPOINT_SEQUENCE_INVALID")
    return {k:v for k,v in doc.items() if k!="checkpoint_digest"}
