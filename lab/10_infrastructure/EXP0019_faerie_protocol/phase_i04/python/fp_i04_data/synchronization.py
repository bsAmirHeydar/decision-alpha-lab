from __future__ import annotations
from fp_i03_time.calendar import snapshot as calendar_snapshot
from fp_i03_time.enums import CalendarSegment
from fp_i03_time.contracts import TimeKernelConfig
from .canonical import canonical_sha256,stable_id
from .constants import M1_MS
from .contracts import *
from .coverage import coverage_interval,gaps_for_axis,source_revision_hash
from .enums import *
from .normalization import normalize_bars
from .revision import classify_revision
from .errors import FPI04Error

def minute_axis(start_utc_ms:int,end_utc_ms:int,policy:ExpectedMinutePolicy,time_config:TimeKernelConfig):
    if start_utc_ms<0 or start_utc_ms%M1_MS or end_utc_ms<=start_utc_ms or end_utc_ms%M1_MS: raise FPI04Error('FP_DRC_SYNC_RANGE_INVALID','range must be aligned half-open M1')
    out=[]; cal={}
    for minute in range(start_utc_ms,end_utc_ms,M1_MS):
        snap=calendar_snapshot(minute,time_config)
        cal[minute]=snap
        if policy is ExpectedMinutePolicy.ALL_REQUESTED_MINUTES or snap.segment in (CalendarSegment.A,CalendarSegment.L,CalendarSegment.N):out.append(minute)
    return tuple(out),cal

def _cell(symbol,minute,bar_map,conflicts,revision_hash,previous_map,coverage_bounds):
    if minute in conflicts:return MinuteCell(symbol,minute,MinuteCellState.CONFLICT,None,'FP_DRC_DUPLICATE_CONFLICT',revision_hash)
    bar=bar_map.get((symbol,minute))
    if bar is None:
        lo,hi=coverage_bounds
        if lo is None or minute<lo or minute>hi:return MinuteCell(symbol,minute,MinuteCellState.OUT_OF_COVERAGE,None,'FP_DRC_M1_OUT_OF_COVERAGE',revision_hash)
        return MinuteCell(symbol,minute,MinuteCellState.MISSING,None,'FP_DRC_M1_MISSING',revision_hash)
    old=previous_map.get((symbol,minute)); state=MinuteCellState.REVISED if old is not None and old.bar_hash!=bar.bar_hash else MinuteCellState.PRESENT
    reason='FP_DRC_M1_REVISED' if state is MinuteCellState.REVISED else 'FP_DRC_M1_PRESENT'
    return MinuteCell(symbol,minute,state,bar,reason,revision_hash)

def synchronize(pair:SymbolPairSpec,bars, start_utc_ms:int,end_utc_ms:int,config:SynchronizerConfig|None=None,time_config:TimeKernelConfig|None=None,previous_bars=(),parent_revision_id='NONE',created_utc_ms=0):
    time_config=time_config or TimeKernelConfig(); config=config or SynchronizerConfig(pair_id=pair.pair_id,calendar_config_hash=time_config.config_hash)
    if config.pair_id!=pair.pair_id: raise FPI04Error('FP_DRC_PAIR_CONFIG_MISMATCH','config pair differs')
    if config.calendar_config_hash!=time_config.config_hash: raise FPI04Error('FP_DRC_CALENDAR_HASH_MISMATCH','calendar config hash differs')
    normalized,resolutions=normalize_bars(pair,tuple(bars),config.closed_bars_only)
    prev_normalized,_=normalize_bars(pair,tuple(previous_bars),config.closed_bars_only) if previous_bars else ((),())
    revision=classify_revision(pair.pair_id,normalized,prev_normalized,parent_revision_id,created_utc_ms)
    axis,calendar=minute_axis(start_utc_ms,end_utc_ms,config.expected_minute_policy,time_config)
    bar_map={(b.canonical_symbol,b.open_utc_ms):b for b in normalized}; prev_map={(b.canonical_symbol,b.open_utc_ms):b for b in prev_normalized}
    conflicts_by_symbol={pair.left.canonical_symbol:set(),pair.right.canonical_symbol:set()}
    for r in resolutions:
        if r.disposition is DuplicateDisposition.CONFLICT: conflicts_by_symbol[r.canonical_symbol].add(r.open_utc_ms)
    revision_hash=revision.revision_hash; rows=[]
    left_minutes=[b.open_utc_ms for b in normalized if b.canonical_symbol==pair.left.canonical_symbol]; right_minutes=[b.open_utc_ms for b in normalized if b.canonical_symbol==pair.right.canonical_symbol]
    left_bounds=(min(left_minutes),max(left_minutes)) if left_minutes else (None,None); right_bounds=(min(right_minutes),max(right_minutes)) if right_minutes else (None,None)
    for minute in axis:
        snap=calendar[minute]
        left=_cell(pair.left.canonical_symbol,minute,bar_map,conflicts_by_symbol[pair.left.canonical_symbol],revision_hash,prev_map,left_bounds)
        right=_cell(pair.right.canonical_symbol,minute,bar_map,conflicts_by_symbol[pair.right.canonical_symbol],revision_hash,prev_map,right_bounds)
        rows.append(AlignedMinute(pair.pair_id,minute,left,right,snap.segment.value,canonical_sha256(snap)))
    left_bars=tuple(b for b in normalized if b.canonical_symbol==pair.left.canonical_symbol)
    right_bars=tuple(b for b in normalized if b.canonical_symbol==pair.right.canonical_symbol)
    lc=coverage_interval(pair.left.canonical_symbol,start_utc_ms,end_utc_ms,left_bars,axis,conflicts_by_symbol[pair.left.canonical_symbol])
    rc=coverage_interval(pair.right.canonical_symbol,start_utc_ms,end_utc_ms,right_bars,axis,conflicts_by_symbol[pair.right.canonical_symbol])
    gaps=gaps_for_axis(pair.left.canonical_symbol,axis,left_bars,revision.revision_id,conflicts_by_symbol[pair.left.canonical_symbol])+gaps_for_axis(pair.right.canonical_symbol,axis,right_bars,revision.revision_id,conflicts_by_symbol[pair.right.canonical_symbol])
    conflicts=tuple(r for r in resolutions if r.disposition is DuplicateDisposition.CONFLICT)
    if conflicts:health=SynchronizationHealth.BLOCKED; reasons=('FP_DRC_DUPLICATE_CONFLICT','FP_DRC_SYNC_BLOCKED')
    elif gaps:health=SynchronizationHealth.DEGRADED; reasons=('FP_DRC_M1_MISSING','FP_DRC_SYNC_DEGRADED')
    else:health=SynchronizationHealth.READY; reasons=('FP_DRC_SYNC_READY',)
    semantic=canonical_sha256({'pair_hash':pair.pair_hash,'config_hash':config.config_hash,'range':[start_utc_ms,end_utc_ms],'rows':[r.row_id for r in rows],'revision':revision.revision_id,'gaps':[g.gap_id for g in gaps],'conflicts':[c.evidence_hash for c in conflicts]})
    result_id=stable_id('FPSYNC',semantic,32)
    return SynchronizationResult(result_id,pair.pair_id,start_utc_ms,end_utc_ms,tuple(rows),lc,rc,tuple(sorted(gaps,key=lambda g:(g.start_utc_ms,g.canonical_symbol))),conflicts,revision,health,tuple(sorted(set(reasons))),semantic)

def snapshot_from_result(result:SynchronizationResult,created_utc_ms:int):
    material={'result_id':result.result_id,'row_ids':[r.row_id for r in result.rows],'revision':result.revision.revision_id,'health':result.health,'reasons':result.reason_codes}
    return PairDatasetSnapshot(stable_id('FPDATA',material,32),result.pair_id,result.start_utc_ms,result.end_utc_ms,tuple(r.row_id for r in result.rows),canonical_sha256(material),result.revision.revision_id,created_utc_ms,result.health,result.reason_codes)
