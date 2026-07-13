from __future__ import annotations
from datetime import date,datetime,timezone
from fp_i02_kernel.enums import WindowKind
from fp_i03_time.calendar import build_session, build_week_from_sunday
from fp_i03_time.enums import CalendarSegment
from fp_i04_data.enums import MinuteCellState
from .canonical import canonical_sha256,stable_id
from .contracts import WindowDescriptor,SymbolWindowAggregate,PairWindowAggregate,WindowStoreConfig
from .enums import WindowBuildState,PairWindowHealth
from .errors import FPI05Error

_SEG={WindowKind.A:CalendarSegment.A,WindowKind.L:CalendarSegment.L,WindowKind.N:CalendarSegment.N}

def descriptor_for_session(pair_id:str,trading_date:date,kind:WindowKind,calendar_config_hash:str):
    if kind not in _SEG: raise FPI05Error('FP_RRC_SESSION_KIND_INVALID','session descriptor requires A/L/N')
    window,_=build_session(trading_date,_SEG[kind])
    material={'pair_id':pair_id,'kind':kind,'trading_date':trading_date.isoformat(),'start':window.start_utc_ms,'end':window.end_utc_ms,'calendar':calendar_config_hash}
    return WindowDescriptor(stable_id('FPWINDESC',material,32),pair_id,kind,trading_date.isoformat(),window.trading_day_id,'',window.start_utc_ms,window.end_utc_ms,window.elapsed_seconds//60,calendar_config_hash,window.window_id)

def descriptor_for_week(pair_id:str,start_sunday:date,calendar_config_hash:str):
    window,_=build_week_from_sunday(start_sunday)
    expected=5*23*60
    material={'pair_id':pair_id,'kind':WindowKind.W,'week_id':window.week_id,'start':window.start_utc_ms,'end':window.end_utc_ms,'calendar':calendar_config_hash}
    return WindowDescriptor(stable_id('FPWINDESC',material,32),pair_id,WindowKind.W,window.end_date,f'NYDAY-{window.end_date}',window.week_id,window.start_utc_ms,window.end_utc_ms,expected,calendar_config_hash,window.window_id)

def _aggregate_symbol(descriptor,rows,symbol,side_name,as_of_utc_ms,revision_id,min_ratio):
    relevant=[r for r in rows if descriptor.start_utc_ms<=r.open_utc_ms<descriptor.end_utc_ms and (descriptor.kind is not WindowKind.W or r.calendar_segment in ('A','L','N'))]
    elapsed_end=min(max(as_of_utc_ms,descriptor.start_utc_ms),descriptor.end_utc_ms)
    expected_elapsed=max(0,(elapsed_end-descriptor.start_utc_ms)//60_000)
    cells=[getattr(r,side_name) for r in relevant if r.open_utc_ms<elapsed_end]
    present=[c.bar for c in cells if c.state in (MinuteCellState.PRESENT,MinuteCellState.REVISED)]
    missing=sum(c.state is MinuteCellState.MISSING for c in cells);ooc=sum(c.state is MinuteCellState.OUT_OF_COVERAGE for c in cells);conflict=sum(c.state is MinuteCellState.CONFLICT for c in cells)
    if conflict: state=WindowBuildState.BLOCKED; reasons=('FP_RRC_WINDOW_CONFLICT','FP_RRC_REFERENCE_BLOCKED')
    elif not present: state=WindowBuildState.MISSING; reasons=('FP_RRC_WINDOW_NO_BARS',)
    elif as_of_utc_ms<descriptor.end_utc_ms: state=WindowBuildState.ACTIVE; reasons=('FP_RRC_WINDOW_ACTIVE',)
    elif missing or ooc or len(present)<descriptor.expected_minutes or len(present)/descriptor.expected_minutes<min_ratio: state=WindowBuildState.INCOMPLETE; reasons=('FP_RRC_WINDOW_INCOMPLETE',)
    else: state=WindowBuildState.COMPLETE; reasons=('FP_RRC_WINDOW_COMPLETE',)
    if present:
        ordered=sorted(present,key=lambda b:b.open_utc_ms); high_bar=min(ordered,key=lambda b:(-b.high,b.open_utc_ms)); low_bar=min(ordered,key=lambda b:(b.low,b.open_utc_ms))
        o,h,l,c=ordered[0].open,max(b.high for b in ordered),min(b.low for b in ordered),ordered[-1].close
        ht,lt=high_bar.open_utc_ms,low_bar.open_utc_ms
        hashes=tuple(sorted({b.bar_hash for b in ordered}))
    else:o=h=l=c=ht=lt=None;hashes=()
    material={'descriptor':descriptor.descriptor_hash,'symbol':symbol,'state':state,'ohlc':[o,h,l,c],'extreme_times':[ht,lt],'counts':[len(present),expected_elapsed,descriptor.expected_minutes,missing,ooc,conflict],'revision':revision_id,'bar_hashes':hashes}
    sem=canonical_sha256(material)
    return SymbolWindowAggregate(stable_id('FPSYM_WINDOW',material,32),descriptor.descriptor_id,symbol,state,o,h,l,c,ht,lt,len(present),expected_elapsed,descriptor.expected_minutes,missing,ooc,conflict,revision_id,hashes,reasons,sem)

def aggregate_pair_window(descriptor,rows,left_symbol,right_symbol,as_of_utc_ms,revision_id,minimum_coverage_ratio=1.0):
    left=_aggregate_symbol(descriptor,rows,left_symbol,'left',as_of_utc_ms,revision_id,minimum_coverage_ratio)
    right=_aggregate_symbol(descriptor,rows,right_symbol,'right',as_of_utc_ms,revision_id,minimum_coverage_ratio)
    if WindowBuildState.BLOCKED in (left.state,right.state): health=PairWindowHealth.BLOCKED; reasons=('FP_RRC_PAIR_WINDOW_BLOCKED',)
    elif left.state!=right.state or left.state in (WindowBuildState.INCOMPLETE,WindowBuildState.MISSING): health=PairWindowHealth.DEGRADED; reasons=('FP_RRC_PAIR_WINDOW_DEGRADED',)
    else: health=PairWindowHealth.READY; reasons=('FP_RRC_PAIR_WINDOW_READY',)
    material={'descriptor':descriptor.descriptor_hash,'left':left.semantic_hash,'right':right.semantic_hash,'health':health,'revision':revision_id}
    sem=canonical_sha256(material)
    return PairWindowAggregate(stable_id('FPPAIR_WINDOW',material,32),descriptor,left,right,health,revision_id,reasons,sem)
