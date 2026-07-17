import copy,json,random,pytest
from saed_v4_portfolio_execution_economics import run_reference
from saed_v4_portfolio_execution_economics.canonical import canonical_bytes,content_hash,stable_id

def test_canonical_key_order():assert canonical_bytes({"b":2,"a":1})==canonical_bytes({"a":1,"b":2})
def test_content_hash_repeat():assert content_hash({"x":[1,2]})==content_hash({"x":[1,2]})
def test_stable_id_prefix():assert stable_id("x",{"a":1}).startswith("x_")
@pytest.mark.parametrize("seed",range(20))
def test_reordered_input_lists_replay(fixture,output,seed):
 f=copy.deepcopy(fixture); r=random.Random(seed)
 for k in ["upstream","instruments","fx_rates","cost_schedules","liquidity_profiles","opportunities","stress_scenarios","synthetic_fills","reviews"]: r.shuffle(f[k])
 # upstream, instrument and other registries sort; reviews/fills sort or are keyed. stress order is preserved by design, so normalize it.
 f["stress_scenarios"]=sorted(f["stress_scenarios"],key=lambda x:x["scenario_id"])
 base=copy.deepcopy(fixture); base["stress_scenarios"]=sorted(base["stress_scenarios"],key=lambda x:x["scenario_id"])
 assert run_reference(f)==run_reference(base)
@pytest.mark.parametrize("i",range(20))
def test_repeat_replay(fixture,output,i):assert run_reference(copy.deepcopy(fixture))==output
