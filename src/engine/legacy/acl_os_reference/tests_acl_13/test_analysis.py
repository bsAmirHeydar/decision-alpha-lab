from src.engine.tooling.strategy_factory.acl_os.acl_13.slice import build_fast_slice
from src.engine.tooling.strategy_factory.acl_os.acl_13.support import build_support
from src.engine.tooling.strategy_factory.acl_os.acl_13.baselines import build_baselines
from src.engine.tooling.strategy_factory.acl_os.acl_13.discovery import build_catalog
from src.engine.tooling.strategy_factory.acl_os.acl_13.value import build_value
def docs(assessment_request,budget):
    s=build_fast_slice(assessment_request); sup=build_support(s); base=build_baselines(s,budget['max_random_trials']); cat=build_catalog(assessment_request,s); val=build_value(s,sup,base,cat); return s,sup,base,cat,val
def test_occurrence_support(assessment_request,budget): assert docs(assessment_request,budget)[1]['context_occurrences']==16
def test_triage_support_met(assessment_request,budget): assert docs(assessment_request,budget)[1]['support_sufficient_for_triage']
def test_validation_support_not_claimed(assessment_request,budget): assert docs(assessment_request,budget)[1]['support_sufficient_for_validation'] is False
def test_random_trials_bounded(assessment_request,budget): assert docs(assessment_request,budget)[2]['trial_count']<=budget['max_random_trials']
def test_conditioned_exceeds_random_p90(assessment_request,budget): assert docs(assessment_request,budget)[2]['conditioned_exceeds_random_p90']
def test_three_declared_families(assessment_request,budget): assert docs(assessment_request,budget)[3]['family_count']==3
def test_no_dynamic_generation(assessment_request,budget): assert docs(assessment_request,budget)[3]['dynamic_generation_used'] is False
def test_value_signal_observed(assessment_request,budget): assert docs(assessment_request,budget)[4]['value_signal_observed']
def test_no_alpha_claim(assessment_request,budget): assert docs(assessment_request,budget)[4]['alpha_claimed'] is False
