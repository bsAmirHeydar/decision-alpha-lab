def test_candidate_results_are_descriptive(build):
    for r in build()['result_bundle']['candidate_results']:
        assert r['descriptive_only'] and r['validation_status']=='NOT_VALIDATED' and not r['promotion_allowed']
def test_diagnostic_candidate_cannot_be_selected(build):
    d=[x for x in build()['result_bundle']['candidate_results'] if x['lane']=='DIAGNOSTIC']; assert len(d)==1 and d[0]['diagnostic_selectable'] is False
def test_baselines_are_present(build):
    origins={x['origin'] for x in build()['result_bundle']['candidate_results']}; assert {'BASELINE','AI','HUMAN'}<=origins
def test_segment_results_bind_candidate_digest(build):
    for r in build()['result_bundle']['candidate_results']: assert r['candidate_digest'].startswith('sha256:') and len(r['segment_result_digests'])==3
