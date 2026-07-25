import pytest
from saed_v4_generative_path_stress_lab.contracts import StateSchemaContract
from saed_v4_generative_path_stress_lab.path_data import validate_real_paths,summary
from saed_v4_generative_path_stress_lab.generators import generate_registry
from saed_v4_generative_path_stress_lab.fidelity import compare
from saed_v4_generative_path_stress_lab.uncertainty import horizon_map
from saed_v4_generative_path_stress_lab.canonical import content_hash

@pytest.fixture(scope='module')
def pair(config,paths):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];syn=generate_registry(real,config['generator_program'],content_hash(paths))['paths'];return real,syn
def test_summary_hash(pair):assert len(summary(pair[0])['summary_hash'])==64
def test_fidelity_fields(config,pair):
    r=compare(pair[0],pair[1],config['fidelity']);assert set(r['metrics'])=={'return_mean_error','return_std_error','tail_quantile_error','autocorrelation_error','spread_error','liquidity_error','regime_occupancy_l1'} and r['positive_evidence_usable'] is False
@pytest.mark.parametrize('key',['return_mean_error','return_std_error','tail_quantile_error','autocorrelation_error','spread_error','liquidity_error','regime_occupancy_l1'])
def test_fidelity_metric_nonnegative(config,pair,key):assert compare(pair[0],pair[1],config['fidelity'])['metrics'][key]>=0
@pytest.mark.parametrize('h',range(1,13))
def test_uncertainty_rows(config,pair,h):
    u=horizon_map(pair[1],config['fidelity']['minimum_trusted_horizon'],config['uncertainty_threshold']);assert u['rows'][h-1]['horizon_step']==h and u['rows'][h-1]['ensemble_return_std']>=0
