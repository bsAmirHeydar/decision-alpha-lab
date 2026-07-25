from .contracts import *
from .canonical import sha256

def _decision(item,cfg):
    if cfg.focus_semantic_id and item.semantic_id!=cfg.focus_semantic_id:return FilterOutcome.EXCLUDED_FOCUS,'FP_FILTER_FOCUS_MISMATCH'
    if item.relation and item.relation not in cfg.relations:return FilterOutcome.EXCLUDED_RELATION,'FP_FILTER_RELATION_EXCLUDED'
    if item.direction not in cfg.directions:return FilterOutcome.EXCLUDED_DIRECTION,'FP_FILTER_DIRECTION_EXCLUDED'
    if cfg.states and item.state not in cfg.states:return FilterOutcome.EXCLUDED_STATE,'FP_FILTER_STATE_EXCLUDED'
    if cfg.dispositions and item.disposition not in cfg.dispositions:return FilterOutcome.EXCLUDED_DISPOSITION,'FP_FILTER_DISPOSITION_EXCLUDED'
    if item.session_kind not in cfg.sessions:return FilterOutcome.EXCLUDED_SESSION,'FP_FILTER_SESSION_EXCLUDED'
    if cfg.symbols and item.symbol not in cfg.symbols:return FilterOutcome.EXCLUDED_SYMBOL,'FP_FILTER_SYMBOL_EXCLUDED'
    if cfg.kinds and item.kind not in cfg.kinds:return FilterOutcome.EXCLUDED_KIND,'FP_FILTER_KIND_EXCLUDED'
    if item.is_historical and not cfg.include_historical:return FilterOutcome.EXCLUDED_HISTORICAL,'FP_FILTER_HISTORICAL_EXCLUDED'
    return FilterOutcome.INCLUDED,'FP_FILTER_INCLUDED'

def apply_filters(items,cfg,source_snapshot_hash):
    included=[];excluded=[]
    for item in items:
        outcome,reason=_decision(item,cfg)
        if outcome is FilterOutcome.INCLUDED: included.append(item)
        else: excluded.append(FilterDecisionRecord(item.semantic_id,outcome,reason,cfg.filter_hash))
    included=tuple(sorted(included,key=lambda x:(x.event_time,x.semantic_id),reverse=True))
    excluded=tuple(sorted(excluded,key=lambda x:x.semantic_id))
    payload={'included':[x.semantic_id for x in included],'excluded':[(x.semantic_id,x.outcome.value) for x in excluded],'filter_hash':cfg.filter_hash,'source_snapshot_hash':source_snapshot_hash}
    return FilterResult(included,excluded,cfg.filter_hash,source_snapshot_hash,sha256(payload))
