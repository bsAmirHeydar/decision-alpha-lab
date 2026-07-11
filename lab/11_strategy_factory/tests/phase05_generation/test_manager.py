import pytest
from strategy_factory_generation import *
from test_manifest import make_manifest
def bundle(n):return GenerationBundle(GenerationCompiler().compile(make_manifest(requested_generation_id=n,run_id=f'run_{n}'),CompilationEvidence(f'd{n}',f'r{n}')))
def test_stage_activate():
    m=GenerationManager();m.stage(bundle(1));a=m.activate(100);assert a.generation.state is GenerationState.ACTIVE and m.activation_count==1

def test_stage_non_warmed_rejected():
    b=bundle(1);b.generation=b.generation.transition(GenerationState.ACTIVE,10)
    with pytest.raises(ValueError):GenerationManager().stage(b)

def test_rollback():
    m=GenerationManager();m.stage(bundle(1));m.activate(10);m.stage(bundle(2));m.activate(20);x=m.rollback(30);assert x.generation.generation_id==1 and m.rollback_count==1

def test_activate_without_staged():
    with pytest.raises(ValueError):GenerationManager().activate(1)
