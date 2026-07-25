from __future__ import annotations
from typing import Any
from .canonical import digest_object,stable_id
from .errors import ContractError
EVENT_MAP={"eligible":"ELIGIBLE","created":"TRIGGERED","triggered":"TRIGGERED","confirmed":"CONFIRMED","invalidated":"INVALIDATED","cancelled":"CANCELLED","canceled":"CANCELLED","expired":"EXPIRED","suppressed":"ABSTAINED","no_trade":"ABSTAINED","blocked":"BLOCKED"}
class LegacyDecisionAdapter:
    """Normalizes supplied legacy evidence; it never imports or calls legacy code."""
    def normalize(self,registration:dict[str,Any],event:dict[str,Any])->dict[str,Any]:
        if registration["adapter_status"]!="REFERENCE_READY":raise ContractError("LCM09B_ADAPTER_BLOCKED")
        raw=str(event.get("event_type","")).lower()
        if raw not in EVENT_MAP:raise ContractError("LCM09B_LEGACY_EVENT_UNKNOWN")
        body={"schema_version":"1.0.0","normalized_event_id":stable_id("LEGACYEVENT",registration["adapter_id"],event.get("legacy_event_id"),event.get("sequence")),"adapter_id":registration["adapter_id"],"setup_id":registration["setup_id"],"legacy_event_id":event["legacy_event_id"],"sequence":int(event["sequence"]),"decision_state":EVENT_MAP[raw],"observed_at":event["observed_at"],"available_at":event["available_at"],"reason_codes":list(event.get("reason_codes",[])),"source_event_digest":event["event_digest"]}
        return {**body,"normalized_event_digest":digest_object(body)}
