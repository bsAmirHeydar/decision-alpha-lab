from .helpers import built

def _lookup(twin,source,scenario):return next(r for r in twin['rows'] if r['source_row_id']==source and r['scenario_id']==scenario)

def test_combined_stress_fill_probability_not_above_nominal():
    *_,twin=built()
    for source in {r['source_row_id'] for r in twin['rows'] if r['action_class']=='ordinary'}:
        assert _lookup(twin,source,'combined_severe')['fill_probability']<=_lookup(twin,source,'nominal')['fill_probability']

def test_combined_stress_latency_not_below_nominal():
    *_,twin=built()
    for source in {r['source_row_id'] for r in twin['rows'] if r['action_class']=='ordinary'}:
        assert _lookup(twin,source,'combined_severe')['total_to_fill_ms']>=_lookup(twin,source,'nominal')['total_to_fill_ms']
