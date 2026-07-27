import pytest
from strategy_factory_generation import *
from .test_manifest import make_manifest
def compile_one(n=1):return GenerationCompiler().compile(make_manifest(requested_generation_id=n),CompilationEvidence('desc_1','req_1'))
def test_compiler_returns_warmed():assert compile_one().state is GenerationState.WARMED

def test_generation_uid_stable():assert compile_one().generation_uid==compile_one().generation_uid

def test_illegal_transition_rejected():
    with pytest.raises(ValueError):compile_one().transition(GenerationState.RETIRED,2000)

def test_activate_and_retire():
    g=compile_one().transition(GenerationState.ACTIVE,2000).transition(GenerationState.RETIRED,3000);assert g.retired_at_utc_msc==3000

def test_compile_requires_ready():
    with pytest.raises(ValueError):GenerationCompiler().compile(make_manifest(),CompilationEvidence('d','r',requirements_ready=False))
