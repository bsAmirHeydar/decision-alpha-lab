from __future__ import annotations
from .canonical import token

_RULES = (
    ("DayeTrader/EXP0018", "EXP0018_DAYE_TRADER_OWNER", "EXP0018_DAYE_TRADER"),
    ("IntermarketDivergenceExecution/CG", "EXP0017_CG_OWNER", "EXP0017_CG"),
    ("IntermarketDivergenceExecution/STC", "EXP0017_STC_OWNER", "EXP0017_STC"),
    ("FlagCountingPhoenix", "FLAG_COUNTING_PHOENIX_OWNER", "FLAG_COUNTING_PHOENIX"),
    ("FaerieProtocol", "EXP0019_FAERIE_PROTOCOL_OWNER", "EXP0019_FAERIE_PROTOCOL"),
    ("EXP0019", "EXP0019_FAERIE_PROTOCOL_OWNER", "EXP0019_FAERIE_PROTOCOL"),
    ("GartalNews", "GARTAL_NEWS_OWNER", "GARTAL_NEWS"),
    ("EXP0013", "EXP0013_RESEARCH_OWNER", "EXP0013_ASTRO_RESEARCH"),
    ("M0001", "M0001_RESEARCH_OWNER", "M0001"),
    ("M0004", "M0004_RESEARCH_OWNER", "M0004"),
    ("M0006", "M0006_RESEARCH_OWNER", "M0006"),
    ("M0007", "M0007_RESEARCH_OWNER", "M0007"),
    ("Common/DAL_ChartObjects", "COMMON_VISUAL_PRIMITIVE_OWNER", "COMMON_VISUAL_PRIMITIVES"),
    ("phase12_5_pipeline_integrity.py", "EXP0017_PIPELINE_INTEGRITY_OWNER", "EXP0017_PIPELINE_INTEGRITY"),
)

def infer_owner(path: str) -> tuple[str, str]:
    normalized = path.replace("\\", "/")
    for marker, owner, subsystem in _RULES:
        if marker.lower() in normalized.lower(): return owner, subsystem
    stem = normalized.rsplit("/", 1)[-1].split(".")[0]
    return f"{token(stem)}_OWNER", token(stem)

def infer_source_event(path: str, surface_kind: str) -> tuple[str, str, str]:
    p=path.lower()
    if surface_kind == "INDICATOR_BUFFER": return "DERIVED_SERIES_EVENT", "BOUND_BY_BUFFER_CONTRACT", "SetIndexBuffer exposes a derived series projection."
    if surface_kind == "REPORT_PROJECTION": return "REPORT_EVENT_RECORD", "BOUND_BY_REPORT_PRODUCER", "Report writer projects a deterministic report record."
    if "faerieprotocol" in p or "exp0019" in p: return "CONTEXT_EVENT_RECORD", "INFERRED_FROM_CANONICAL_CONTEXT_PACKAGE", "EXP0019 visual projection is context-event based."
    if "dayetrader" in p or "exp0018" in p: return "CONTEXT_EVENT_RECORD", "INFERRED_FROM_CONTEXT_VISUAL_MANAGER", "EXP0018 visual managers project Context state."
    if "intermarketdivergenceexecution" in p or "exp0017" in p: return "SETUP_EVENT_RECORD", "INFERRED_FROM_SETUP_LEDGER", "Intermarket divergence visuals project Setup evidence."
    if "flagcountingphoenix" in p: return "SETUP_EVENT_RECORD", "INFERRED_FROM_SETUP_PHASE", "Flag-counting visual hooks project Setup observations."
    if "gartalnews" in p: return "EXTERNAL_CALENDAR_EVENT", "INFERRED_FROM_NEWS_TIMELINE", "News timeline visuals project external calendar events."
    if "dal_chartobjects" in p: return "CALLER_BOUND_CANONICAL_EVENT", "CONTRACTUAL_CALLER_BINDING_REQUIRED", "Shared primitive must be bound by the caller to a canonical event."
    if any(x in p for x in ("m0001", "m0004", "m0006", "m0007", "exp0013", "astro")):
        return "RESEARCH_OBSERVATION_EVENT", "INFERRED_FROM_RESEARCH_SURFACE", "Research visual surface projects an observation event."
    return "UNKNOWN_CANONICAL_EVENT", "BLOCKED", "No deterministic source-event mapping rule matched the source path."
