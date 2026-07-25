import copy,pytest
from saed_v4_generative_path_stress_lab.contracts import StateSchemaContract
from saed_v4_generative_path_stress_lab.path_data import validate_real_paths
from saed_v4_generative_path_stress_lab.generators import generate_registry
from saed_v4_generative_path_stress_lab.stress import apply_stress,compose_stress_library
from saed_v4_generative_path_stress_lab.invariants import inspect_path,inspect_paths
from saed_v4_generative_path_stress_lab.canonical import content_hash

@pytest.fixture(scope='module')
def generated(config,paths):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];return generate_registry(real,config['generator_program'],content_hash(paths))['paths']
@pytest.mark.parametrize('family',['gap_down','gap_up','volatility_burst','liquidity_collapse','spread_blowout','chop_reversal','regime_break','execution_degradation'])
def test_stress_deterministic_and_labeled(config,generated,family):
    a=apply_stress(generated[0],family,0.25);b=apply_stress(generated[0],family,0.25)
    assert a==b and a['stress_labels'][-1]['family']==family and a['origin']=='synthetic_stress'
@pytest.mark.parametrize('family',['gap_down','gap_up','volatility_burst','liquidity_collapse','spread_blowout','chop_reversal','regime_break','execution_degradation'])
def test_stress_invariants(config,generated,family):assert inspect_path(apply_stress(generated[0],family,0.25),config['path_invariants'])['passed']
def test_library_bound(config,generated):
    x=compose_stress_library(generated[:4],config['stress_program']);assert x['path_count']<=config['stress_program']['maximum_stress_paths'] and inspect_paths(x['paths'],config['path_invariants'])['passed']
def test_bad_geometry_detected(config,generated):
    p=copy.deepcopy(generated[0]);p['rows'][2]['low']=p['rows'][2]['high']+1;assert not inspect_path(p,config['path_invariants'])['passed']
def test_bad_timestamp_detected(config,generated):
    p=copy.deepcopy(generated[0]);p['rows'][2]['timestamp']=p['rows'][1]['timestamp'];assert not inspect_path(p,config['path_invariants'])['passed']
