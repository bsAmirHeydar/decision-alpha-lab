import pytest
from dataclasses import replace
from strategy_factory_trainers_v3.golden import build_case
from strategy_factory_trainers_v3.enums import TaskKind,CalibrationKind
from strategy_factory_trainers_v3.registry import TrainerRegistry
from strategy_factory_trainers_v3.orchestrator import TaskOrchestrator
from strategy_factory_classical_v3 import *
pytest.importorskip('sklearn')
def run(a,task=TaskKind.BINARY_CLASSIFICATION):
 s,rows,p=build_case(task);d=BY_ID[a];r=TrainerRegistry();register_classical_trainers(r);cfg=replace(p.trainer,trainer_id=d.trainer_id,trainer_version=d.trainer_version,hyperparameters=d.default_hyperparameters,calibration_kind=CalibrationKind.IDENTITY if d.probability_output else CalibrationKind.NONE);return TaskOrchestrator(r).run(replace(p,trainer=cfg),s,rows)
def test_logistic_through_orchestrator():
 a=run('logistic_regression');assert a.final_trial.status.value=='succeeded';assert all(0<=x.outputs[0]<=1 for x in a.final_test_predictions.records)
def test_tree_through_orchestrator():assert run('decision_tree_classifier').artifact_manifest.trainer_descriptor_hash
def test_forest_deterministic():assert run('random_forest_classifier').oof_predictions.evidence_hash==run('random_forest_classifier').oof_predictions.evidence_hash
def test_gaussian_nb_probability():assert all(0<=x.outputs[0]<=1 for x in run('gaussian_nb').final_test_predictions.records)
def test_ridge_regression():assert run('ridge_regression',TaskKind.REGRESSION).final_trial.status.value=='succeeded'
def test_huber_regression():assert run('huber_regression',TaskKind.REGRESSION).final_trial.status.value=='succeeded'
