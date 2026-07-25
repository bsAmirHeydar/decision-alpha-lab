from __future__ import annotations
from datetime import date,timedelta
from fp_i02_kernel.enums import WindowKind,LookbackPolicy
from .canonical import canonical_sha256,stable_id
from .contracts import CalendarDaySelectionItem,CalendarDaySelection
from .enums import SelectorDisposition,WindowBuildState
from .errors import FPI05Error

def select_prior_n_calendar_days(anchor_trading_date:str,depth:int,pair_windows,store_snapshot_hash:str):
    try: anchor=date.fromisoformat(anchor_trading_date)
    except ValueError as exc: raise FPI05Error('FP_RRC_SELECTOR_DATE_INVALID','anchor trading date must be ISO date') from exc
    index={(w.descriptor.trading_date,w.descriptor.kind):w for w in pair_windows}
    items=[]
    for offset in range(1,depth+1):
        target=(anchor-timedelta(days=offset)).isoformat(); w=index.get((target,WindowKind.N))
        if w is None: disposition=SelectorDisposition.DATE_MISSING; pw=did=''; reason='FP_RRC_CALENDAR_DATE_MISSING'
        elif WindowBuildState.BLOCKED in (w.left.state,w.right.state): disposition=SelectorDisposition.WINDOW_BLOCKED;pw=w.pair_window_id;did=w.descriptor.descriptor_id;reason='FP_RRC_SELECTED_WINDOW_BLOCKED'
        elif not w.completed: disposition=SelectorDisposition.WINDOW_INCOMPLETE;pw=w.pair_window_id;did=w.descriptor.descriptor_id;reason='FP_RRC_SELECTED_WINDOW_INCOMPLETE'
        else: disposition=SelectorDisposition.SELECTED;pw=w.pair_window_id;did=w.descriptor.descriptor_id;reason='FP_RRC_CALENDAR_OFFSET_SELECTED'
        material={'offset':offset,'target':target,'disposition':disposition,'pair_window_id':pw,'descriptor_id':did}
        items.append(CalendarDaySelectionItem(offset,target,WindowKind.N,disposition,pw,did,reason,canonical_sha256(material)))
    material={'anchor':anchor_trading_date,'depth':depth,'items':[i.evidence_hash for i in items],'store':store_snapshot_hash,'policy':LookbackPolicy.CALENDAR_DAY_DEPTH}
    return CalendarDaySelection(stable_id('FP_N_SELECTOR',material,32),anchor_trading_date,depth,tuple(items),LookbackPolicy.CALENDAR_DAY_DEPTH,store_snapshot_hash,canonical_sha256(material))
