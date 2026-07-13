from fp_i06_relations.conformance import run_conformance

def test_conformance_checks():
    report=run_conformance();checks=report['checks']
    assert checks['compiled_relation_count']==9
    assert checks['compiled_side_plan_count']==18
    assert checks['candidate_direction']=='BEARISH'
    assert checks['same_m1_outcome']=='SYMMETRIC_SAME_M1'
    assert checks['ww_compiled'] is False
