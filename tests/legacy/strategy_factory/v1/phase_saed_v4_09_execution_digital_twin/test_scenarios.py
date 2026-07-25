from helpers import built

def _row(twin,source,scenario):return next(r for r in twin['rows'] if r['source_row_id']==source and r['scenario_id']==scenario)

def test_latency_stress_increases_latency():
    *_,twin=built();source=next(r['source_row_id'] for r in twin['rows'] if r['action_class']=='ordinary');assert _row(twin,source,'latency_x3')['total_to_fill_ms']>_row(twin,source,'nominal')['total_to_fill_ms']

def test_spread_stress_never_reduces_incremental_spread():
    *_,twin=built();sources={r['source_row_id'] for r in twin['rows']};assert all(_row(twin,s,'spread_x2')['incremental_spread_points']>=_row(twin,s,'nominal')['incremental_spread_points'] for s in sources)

def test_partial_fill_cap_is_enforced():
    *_,twin=built();assert all(r['fill_fraction']<=.6 for r in twin['rows'] if r['scenario_id']=='queue_x4_partial')
