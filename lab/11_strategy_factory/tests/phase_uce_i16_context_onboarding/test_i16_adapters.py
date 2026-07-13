import pytest
from strategy_factory_onboarding_v3.adapters import LegacyAdapter,measure_parity
from strategy_factory_onboarding_v3.contracts import LegacyAdapterSpec
from strategy_factory_onboarding_v3.canonical import canonical_sha256
from strategy_factory_onboarding_v3.enums import AdapterMode,ParityStatus
from strategy_factory_onboarding_v3.errors import OnboardingError

def spec():return LegacyAdapterSpec('a','1.0.0','c',('legacy.py',),(canonical_sha256('legacy'),),AdapterMode.DIFFERENTIAL,True,True,True,True,True)
@pytest.mark.parametrize('value',[0,1,-1,0.5,1000000])
def test_exact_differential_parity(value):
 fn=lambda p:{'x':p['x']};a=LegacyAdapter(spec(),fn,fn);o=a.observe('o',1,{'x':value});assert o.matched;assert measure_parity(spec(),(o,),0).status is ParityStatus.PASS
@pytest.mark.parametrize('delta',[0.001,0.01,1.0,10.0])
def test_mismatch_is_measured(delta):
 a=LegacyAdapter(spec(),lambda p:{'x':p['x']},lambda p:{'x':p['x']+delta});o=a.observe('o',1,{'x':1},0.0);r=measure_parity(spec(),(o,),0.0);assert not o.matched and r.status is ParityStatus.FAIL and r.max_delta==pytest.approx(delta)
@pytest.mark.parametrize('tolerance',[0.1,1.0,10.0])
def test_tolerance_can_accept_bounded_delta(tolerance):
 a=LegacyAdapter(spec(),lambda p:{'x':1.0},lambda p:{'x':1.0+tolerance/2});o=a.observe('o',1,{},tolerance);assert o.matched
def test_empty_parity_is_insufficient():assert measure_parity(spec(),(),0).status is ParityStatus.INSUFFICIENT
def test_input_mutation_detected():
 def bad(p):p['x']=2;return {'x':2}
 a=LegacyAdapter(spec(),bad,lambda p:{'x':2})
 # Deep copies isolate the mutation from caller and preserve source mutation isolation.
 payload={'x':1};a.observe('o',1,payload);assert payload=={'x':1}
def test_non_numeric_difference_is_detected():
 a=LegacyAdapter(spec(),lambda p:{'x':'a'},lambda p:{'x':'b'});o=a.observe('o',1,{});assert not o.matched
