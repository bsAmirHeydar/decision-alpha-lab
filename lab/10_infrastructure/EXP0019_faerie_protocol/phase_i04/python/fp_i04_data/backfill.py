from __future__ import annotations
from .canonical import stable_id
from .contracts import BackfillRequest,GapInterval,SynchronizerConfig
from .enums import BackfillAction,GapReason

def plan_backfill(gaps,config:SynchronizerConfig):
    out=[]
    for gap in sorted(gaps,key=lambda g:(g.start_utc_ms,g.canonical_symbol)):
        if gap.reason is GapReason.DUPLICATE_CONFLICT:
            action=BackfillAction.BLOCK; reason='FP_DRC_BACKFILL_BLOCKED_CONFLICT'
        elif gap.missing_minutes>config.maximum_backfill_minutes:
            action=BackfillAction.FULL_REBUILD; reason='FP_DRC_BACKFILL_LIMIT_EXCEEDED'
        else:
            action=BackfillAction.FETCH_RANGE; reason='FP_DRC_BACKFILL_RANGE_PLANNED'
        material={'symbol':gap.canonical_symbol,'start':gap.start_utc_ms,'end':gap.end_utc_ms,'action':action,'gap_id':gap.gap_id,'config_hash':config.config_hash}
        out.append(BackfillRequest(stable_id('FPBACKFILL',material,32),gap.canonical_symbol,gap.start_utc_ms,gap.end_utc_ms,gap.missing_minutes,action,reason,0 if action is BackfillAction.BLOCK else 10))
    return tuple(out)
