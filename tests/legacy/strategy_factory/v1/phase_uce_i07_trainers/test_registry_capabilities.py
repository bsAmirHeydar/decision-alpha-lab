import pytest
from strategy_factory_trainers_v3 import *
from strategy_factory_trainers_v3.golden import build_case
def test_registry_exact_and_three_families():
 r=TrainerRegistry();register_reference_trainers(r);assert len(r.snapshot())==3
 with pytest.raises(CapabilityError):r.resolve_exact('uce.reference.prior_binary','9.0.0')
def test_unsupported_pair_fails_preflight():
 r=TrainerRegistry();register_reference_trainers(r);s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);d=r.resolve_exact('uce.reference.mean_regression','1.0.0').descriptor;report=CapabilityMatcher.evaluate(d,p.task,s,p.resources);assert not report.compatible and 'unsupported_task' in {x.code for x in report.findings}

def test_registry_freezes_when_orchestrator_binds():
 r=TrainerRegistry();register_reference_trainers(r);TaskOrchestrator(r);assert r.frozen
 with pytest.raises(CapabilityError):r.register(PriorBinaryTrainer)
