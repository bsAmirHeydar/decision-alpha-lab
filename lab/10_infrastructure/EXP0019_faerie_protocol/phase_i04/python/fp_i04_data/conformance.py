from __future__ import annotations
from fp_i03_time.contracts import TimeKernelConfig
from .backfill import plan_backfill
from .cursor import advance_cursor,empty_cursor
from .golden import golden_bars,golden_config,golden_pair
from .synchronization import synchronize,snapshot_from_result
from .revision import revision_impact

def run_conformance():
    start=1783900800000;pair=golden_pair();config=golden_config();tc=TimeKernelConfig();bars=golden_bars(start,5)
    first=synchronize(pair,bars,start,start+300000,config,tc,created_utc_ms=start+999999)
    second=synchronize(pair,bars,start,start+300000,config,tc,created_utc_ms=start+999999)
    cursor=advance_cursor(empty_cursor(pair.pair_id),first);snapshot=snapshot_from_result(first,start+999999);impact=revision_impact(first.revision,first.rows)
    checks={
      'deterministic_result':first==second,
      'five_rows':len(first.rows)==5,
      'both_present':first.both_present_minutes==5,
      'ready':first.health.value=='READY',
      'no_gaps':not first.gaps,
      'no_conflicts':not first.conflicts,
      'cursor_active':cursor.state.value=='ACTIVE',
      'snapshot_hash':len(snapshot.semantic_hash)==64,
      'impact_hashes':len(impact.unaffected_prefix_hash)==64 and len(impact.changed_suffix_hash)==64,
      'no_backfill':not plan_backfill(first.gaps,config),
    }
    return {'phase':'FP-I04','check_count':len(checks),'passed':all(checks.values()),'checks':checks,'result_id':first.result_id,'semantic_hash':first.semantic_hash,'revision_id':first.revision.revision_id}
