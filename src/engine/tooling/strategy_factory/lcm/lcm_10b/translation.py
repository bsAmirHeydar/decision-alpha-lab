from __future__ import annotations
from typing import Any
from .execution_intent import build_execution_intent
ALIASES={"direction":"side","ticker":"symbol","instrument":"symbol","timestamp":"decision_time","known_time":"availability_time","qty":"volume","lots":"volume"}
RECOGNIZED={"decision_id","side","symbol","decision_time","availability_time","entry","stop","targets","volume_request","expiry","cancellation","management","source_evidence","unsupported_fields","direction","ticker","instrument","timestamp","known_time","qty","lots"}
def translate_legacy_request(package:dict[str,Any],legacy:dict[str,Any])->dict[str,Any]:
    normalized=dict(legacy)
    for old,new in ALIASES.items():
        if new not in normalized and old in normalized:normalized[new]=normalized[old]
    if "volume_request" not in normalized and ("qty" in normalized or "lots" in normalized):normalized["volume_request"]={"mode":"EXPLICIT","value":normalized.get("qty",normalized.get("lots")),"unit":"LOTS" if "lots" in normalized else "UNITS"}
    unknown=sorted(set(legacy)-RECOGNIZED);normalized["unsupported_fields"]=sorted(set(normalized.get("unsupported_fields",[])+unknown))
    intent=build_execution_intent(package,normalized)
    if unknown:intent["rejection_reasons"]=sorted(set(intent["rejection_reasons"]+["UNTRANSLATABLE_LEGACY_FIELDS"]));intent["validation_status"]="BLOCKED"
    return intent
