from __future__ import annotations
import re
from .canonical import stable_id
from .constants import OBJECT_TYPES_PRICE_ONLY, OBJECT_TYPES_SCREEN, OBJECT_TYPES_TIME_ONLY
from .models import AnchorContract, VisualSite

def _current_bar_risk(exprs: list[str]) -> bool:
    text=" ".join(exprs).lower()
    patterns=(r"\[[ ]*0[ ]*\]",r"itime\([^,]+,[^,]+,[ ]*0[ ]*\)",r"timecurrent\(",r"rates_total[ ]*-[ ]*1",r"current_bar")
    return any(re.search(p,text) for p in patterns)

def build_anchor_contract(site: VisualSite) -> AnchorContract:
    args=list(site.raw_arguments); blockers=[]
    if site.surface_kind=="INDICATOR_BUFFER":
        kind="SERIES_INDEX"; t1="BUFFER_INDEX_TO_BAR_TIME"; p1=site.observed_name_expression; t2=p2=None
    elif site.surface_kind=="REPORT_PROJECTION":
        kind="REPORT_OUTPUT"; t1="REPORT_GENERATION_INPUT_DIGEST"; p1=None; t2=p2=None
    elif site.object_type in OBJECT_TYPES_SCREEN:
        kind="PIXEL_CORNER"; t1=p1=t2=p2=None
    elif site.object_type in OBJECT_TYPES_TIME_ONLY:
        kind="TIME_ONLY"; t1=args[4] if len(args)>4 else "UNKNOWN"; p1=t2=p2=None
    elif site.object_type in OBJECT_TYPES_PRICE_ONLY:
        kind="PRICE_ONLY"; p1=args[5] if len(args)>5 else (args[4] if len(args)>4 else "UNKNOWN"); t1=t2=p2=None
    else:
        kind="TIME_PRICE"; t1=args[4] if len(args)>4 else "UNKNOWN"; p1=args[5] if len(args)>5 else "UNKNOWN"; t2=args[6] if len(args)>6 else None; p2=args[7] if len(args)>7 else None
    evidence=[x for x in (t1,p1,t2,p2) if x]
    if site.surface_kind=="REPORT_PROJECTION": availability="BOUND_REPORT_INPUT"
    elif kind=="PIXEL_CORNER": availability="NOT_MARKET_TIME_ANCHORED"
    elif _current_bar_risk(evidence):
        availability="CURRENT_BAR_OR_RUNTIME_UNKNOWN"; blockers.append(stable_id("VISBLOCK",site.visual_object_id,"CURRENT_BAR_CONFIRMATION"))
    elif site.source_event_binding_status in {"BOUND_BY_BUFFER_CONTRACT","BOUND_BY_REPORT_PRODUCER","INFERRED_FROM_CANONICAL_CONTEXT_PACKAGE","INFERRED_FROM_SETUP_LEDGER","INFERRED_FROM_CONTEXT_VISUAL_MANAGER"}: availability="EVENT_AVAILABILITY_TIME_BOUND"
    else: availability="CALLER_BOUND_AVAILABILITY_TIME"
    chart_expr=site.chart_scope_expression.lower()
    if site.surface_kind=="REPORT_PROJECTION": projection="REPORT_SURFACE"
    elif chart_expr in {"0","chartid()"} or "chartid" in chart_expr: projection="HOST_OR_EXPLICIT_CHART"
    elif chart_expr=="indicator_window": projection="INDICATOR_WINDOW"
    else: projection="EXPLICIT_CHART_EXPRESSION"
    source_candle="EVENT_BOUND"
    if availability=="CURRENT_BAR_OR_RUNTIME_UNKNOWN": source_candle="UNKNOWN_BLOCKING"
    if site.surface_kind=="INDICATOR_BUFFER": source_candle="BUFFER_SERIES_INDEXED"
    extension="NONE"
    if site.object_type=="OBJ_TREND": extension="OBSERVED_RAY_POLICY_REQUIRES_PROPERTY_SCAN"
    elif site.object_type=="OBJ_RECTANGLE": extension="FIXED_TWO_POINT_REGION"
    status="BLOCKED" if blockers else "PASS"
    return AnchorContract(stable_id("VISANCH",site.visual_object_id,kind,t1,p1,t2,p2),site.visual_object_id,kind,projection,source_candle,availability,t1,p1,t2,p2,extension,"STYLE_MUST_NOT_CHANGE_SOURCE_EVENT_SEMANTICS",status,tuple(blockers))
