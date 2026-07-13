from __future__ import annotations
from dataclasses import replace
from functools import lru_cache
from datetime import date,timedelta
from fp_i02_kernel.enums import WindowKind,RelationCode,PriceSide
from fp_i03_time.contracts import TimeKernelConfig
from fp_i03_time.calendar import build_session
from fp_i03_time.enums import CalendarSegment
from fp_i04_data.golden import golden_pair,bar
from fp_i04_data.synchronization import synchronize
from fp_i04_data.contracts import SynchronizerConfig
from fp_i04_data.enums import ExpectedMinutePolicy
from fp_i05_reference.contracts import WindowStoreConfig
from fp_i05_reference.window_builder import descriptor_for_session,aggregate_pair_window
from fp_i05_reference.reference_engine import derive_reference_set
from fp_i05_reference.store import build_store_snapshot
from fp_i05_reference.selector import select_prior_n_calendar_days
from .contracts import RelationCompilerConfig
from .registry import registry_hash
from .compiler import compile_relations

def _window(pair,day,kind,tc,base_left=5000.0,base_right=20000.0):
    segment={WindowKind.A:CalendarSegment.A,WindowKind.L:CalendarSegment.L,WindowKind.N:CalendarSegment.N}[kind]
    sess,_=build_session(day,segment);bars=[]
    for i,minute in enumerate(range(sess.start_utc_ms,sess.end_utc_ms,60_000)):
        bars.extend((bar('ES',minute,base_left+i*.25,2*i),bar('NQ',minute,base_right+i*.5,2*i+1)))
    cfg=SynchronizerConfig(pair_id=pair.pair_id,expected_minute_policy=ExpectedMinutePolicy.ALL_REQUESTED_MINUTES,calendar_config_hash=tc.config_hash)
    sync=synchronize(pair,bars,sess.start_utc_ms,sess.end_utc_ms,cfg,tc,created_utc_ms=sess.end_utc_ms)
    desc=descriptor_for_session(pair.pair_id,day,kind,tc.config_hash)
    agg=aggregate_pair_window(desc,sync.rows,pair.left.canonical_symbol,pair.right.canonical_symbol,sess.end_utc_ms,sync.revision.revision_id)
    refs=derive_reference_set(agg,sess.end_utc_ms)
    return agg,refs,sync

@lru_cache(maxsize=8)
def golden_store_and_report(depth=3):
    tc=TimeKernelConfig();pair=golden_pair();anchor=date(2026,7,14);windows=[];refs=[];syncs={}
    for offset in range(depth,0,-1):
        day=anchor-timedelta(days=offset);agg,r,s=_window(pair,day,WindowKind.N,tc,4950+offset*10,19800+offset*20);windows.append(agg);refs.extend(r.references);syncs[(day.isoformat(),WindowKind.N)]=s
    for kind,bl,br in ((WindowKind.A,5000,20000),(WindowKind.L,5010,20020),(WindowKind.N,5020,20040)):
        agg,r,s=_window(pair,anchor,kind,tc,bl,br);windows.append(agg);refs.extend(r.references);syncs[(anchor.isoformat(),kind)]=s
    store_cfg=WindowStoreConfig('FP-CONTEXT-001',pair.pair_id,tc.config_hash,'b'*64,calendar_day_depth=depth)
    snapshot=build_store_snapshot(store_cfg,'FPI04DATASET',windows[-1].source_revision_id,windows,refs,windows[-1].descriptor.end_utc_ms)
    selection=select_prior_n_calendar_days(anchor.isoformat(),depth,snapshot.pair_windows,snapshot.semantic_hash)
    config=RelationCompilerConfig('FP-CONTEXT-001',pair.pair_id,registry_hash(),snapshot.semantic_hash)
    report=compile_relations(config,snapshot,anchor.isoformat(),selection)
    return tc,pair,anchor,snapshot,selection,config,report,syncs
