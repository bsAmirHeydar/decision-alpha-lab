import pytest
from strategy_factory_onboarding_v3.golden import golden_spec
from strategy_factory_onboarding_v3.tournament_template import default_template,compile_template,STAGES
from strategy_factory_onboarding_v3.errors import OnboardingError

def test_template_repeats():
 s=golden_spec();a=default_template(s);b=default_template(s);assert a.template_hash==b.template_hash and compile_template(a).compiled_hash==compile_template(b).compiled_hash

def test_template_has_full_pipeline():
 c=compile_template(default_template(golden_spec()));assert c.stage_ids==STAGES;assert len(c.artifact_identity_map)==9
@pytest.mark.parametrize('stage',STAGES)
def test_every_stage_is_identity_bound(stage):
 c=compile_template(default_template(golden_spec()));assert len(c.artifact_identity_map[stage])==64
@pytest.mark.parametrize('seed',[0,1,42,160016,999999])
def test_seed_is_identity_relevant(seed):
 s=golden_spec();a=default_template(s,seed);b=default_template(s,seed+1);assert a.template_hash!=b.template_hash
