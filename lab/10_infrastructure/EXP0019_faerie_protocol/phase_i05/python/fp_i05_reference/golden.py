from __future__ import annotations
from datetime import date,datetime,timezone
from fp_i02_kernel.enums import WindowKind
from fp_i03_time.contracts import TimeKernelConfig
from fp_i03_time.calendar import build_session
from fp_i03_time.enums import CalendarSegment
from fp_i04_data.golden import golden_pair,bar
from fp_i04_data.synchronization import synchronize
from fp_i04_data.contracts import SynchronizerConfig
from fp_i04_data.enums import ExpectedMinutePolicy
from .contracts import WindowStoreConfig
from .window_builder import descriptor_for_session,aggregate_pair_window
from .reference_engine import derive_reference_set

def golden_completed_n_window():
    tc=TimeKernelConfig();pair=golden_pair();day=date(2026,7,13);sess,_=build_session(day,CalendarSegment.N)
    bars=[]
    for i,minute in enumerate(range(sess.start_utc_ms,sess.end_utc_ms,60_000)):
        bars.extend((bar('ES',minute,5000+i*.25,2*i),bar('NQ',minute,20000+i*.5,2*i+1)))
    cfg=SynchronizerConfig(pair_id=pair.pair_id,expected_minute_policy=ExpectedMinutePolicy.ALL_REQUESTED_MINUTES,calendar_config_hash=tc.config_hash)
    result=synchronize(pair,bars,sess.start_utc_ms,sess.end_utc_ms,cfg,tc,created_utc_ms=sess.end_utc_ms)
    desc=descriptor_for_session(pair.pair_id,day,WindowKind.N,tc.config_hash)
    agg=aggregate_pair_window(desc,result.rows,pair.left.canonical_symbol,pair.right.canonical_symbol,sess.end_utc_ms,result.revision.revision_id)
    refs=derive_reference_set(agg,sess.end_utc_ms)
    store_cfg=WindowStoreConfig('FP-CONTEXT-001',pair.pair_id,tc.config_hash,'b'*64)
    return store_cfg,result,desc,agg,refs
