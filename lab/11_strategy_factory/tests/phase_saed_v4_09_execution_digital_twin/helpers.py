from conftest import load
from saed_v4_execution_twin.models import ExecutionTwinProfile
from saed_v4_execution_twin.twin import build_execution_twin

def inputs():
    cube=load('lab/11_strategy_factory/artifacts/saed_v4_08/GOLDEN_OUTCOME_CUBE.JSON')
    handoff=load('lab/11_strategy_factory/artifacts/saed_v4_08/V4_08_TO_V4_09_HANDOFF.JSON')
    mapping=load('lab/11_strategy_factory/examples/saed_v4_09/execution_twin_profile.json')
    return cube,handoff,mapping

def built():
    cube,handoff,mapping=inputs();profile=ExecutionTwinProfile.from_mapping(mapping)
    return cube,handoff,profile,build_execution_twin(cube,handoff,profile)
