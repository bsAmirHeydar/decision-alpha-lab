import pytest
from saed_v4_generative_path_stress_lab.contracts import StateSchemaContract,GeneratorProgramContract
from saed_v4_generative_path_stress_lab.path_data import validate_real_paths
from saed_v4_generative_path_stress_lab.generators import generate_family,generate_registry
from saed_v4_generative_path_stress_lab.watermark import validate
from saed_v4_generative_path_stress_lab.canonical import content_hash

@pytest.mark.parametrize('family',['moving_block_bootstrap','regime_markov','latent_linear_ensemble','residual_flow_reference'])
def test_family_deterministic(config,paths,family):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];h=content_hash(paths)
    a=generate_family(family,0,real,config['generator_program'],h);b=generate_family(family,0,real,config['generator_program'],h)
    assert a==b and validate(a['watermark']) and len(a['rows'])==config['generator_program']['horizon']
@pytest.mark.parametrize('family',['moving_block_bootstrap','regime_markov','latent_linear_ensemble','residual_flow_reference'])
def test_family_changes_by_index(config,paths,family):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];h=content_hash(paths)
    assert generate_family(family,0,real,config['generator_program'],h)['path_id']!=generate_family(family,1,real,config['generator_program'],h)['path_id']
def test_registry_counts(config,paths):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];r=generate_registry(real,config['generator_program'],content_hash(paths))
    expected=config['generator_program']['paths_per_family']*(3+config['generator_program']['ensemble_members'])
    assert r['path_count']==expected and all(validate(p['watermark']) for p in r['paths'])
@pytest.mark.parametrize('i',range(12))
def test_generated_paths_research_only(config,paths,i):
    real=validate_real_paths(paths,StateSchemaContract.from_mapping(config['state_schema']))['paths'];r=generate_registry(real,config['generator_program'],content_hash(paths));p=r['paths'][i]
    assert p['research_only'] and p['watermark']['positive_promotion_evidence'] is False and p['watermark']['runtime_eligible'] is False
