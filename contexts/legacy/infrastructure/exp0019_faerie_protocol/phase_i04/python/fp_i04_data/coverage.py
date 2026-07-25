from __future__ import annotations
from .canonical import canonical_sha256
from .constants import M1_MS
from .contracts import CoverageInterval,GapInterval,M1Bar
from .enums import CoverageState,GapReason

def source_revision_hash(bars):
    return canonical_sha256([(b.open_utc_ms,b.bar_hash,b.source_sequence,b.source_revision) for b in sorted(bars,key=lambda x:(x.open_utc_ms,x.bar_hash))])

def coverage_interval(symbol,start,end,bars,expected_axis=None,conflict_minutes=()):
    by_min={b.open_utc_ms:b for b in bars if b.canonical_symbol==symbol and start<=b.open_utc_ms<end}
    total=(end-start)//M1_MS; axis=tuple(range(start,end,M1_MS)) if expected_axis is None else tuple(expected_axis); expected=len(axis); excluded=total-expected; present=sum(1 for minute in axis if minute in by_min); conflicts=set(conflict_minutes)
    if conflicts: state=CoverageState.CONFLICTED; reason='FP_DRC_COVERAGE_CONFLICTED'
    elif present==0: state=CoverageState.EMPTY; reason='FP_DRC_COVERAGE_EMPTY'
    elif present==expected: state=CoverageState.COMPLETE; reason='FP_DRC_COVERAGE_COMPLETE'
    else: state=CoverageState.PARTIAL; reason='FP_DRC_COVERAGE_PARTIAL'
    return CoverageInterval(symbol,start,end,present,expected,excluded,state,source_revision_hash(tuple(by_min.values())),reason)

def gaps_for_axis(symbol,axis,bars,revision,conflict_minutes=()):
    present={b.open_utc_ms for b in bars if b.canonical_symbol==symbol}; conflicts=set(conflict_minutes); missing=[]
    lo=min(present) if present else None; hi=max(present) if present else None
    for minute in axis:
        if minute in present: continue
        if minute in conflicts: reason=GapReason.DUPLICATE_CONFLICT
        elif lo is None or minute<lo: reason=GapReason.BEFORE_COVERAGE
        elif minute>hi: reason=GapReason.AFTER_COVERAGE
        else: reason=GapReason.SOURCE_MISSING
        missing.append((minute,reason))
    out=[]
    if not missing:return ()
    run_start,prev,reason=missing[0][0],missing[0][0],missing[0][1]
    for minute,next_reason in missing[1:]:
        if minute!=prev+M1_MS or next_reason!=reason:
            end=prev+M1_MS; material={'symbol':symbol,'start':run_start,'end':end,'reason':reason,'revision':revision}
            out.append(GapInterval(symbol,run_start,end,(end-run_start)//M1_MS,reason,revision,canonical_sha256(material)))
            run_start,reason=minute,next_reason
        prev=minute
    end=prev+M1_MS; material={'symbol':symbol,'start':run_start,'end':end,'reason':reason,'revision':revision}
    out.append(GapInterval(symbol,run_start,end,(end-run_start)//M1_MS,reason,revision,canonical_sha256(material)))
    return tuple(out)
