from dataclasses import replace
from strategy_factory_trainers_v3.golden import build_case
from strategy_factory_trainers_v3.enums import TaskKind
from strategy_factory_trainers_v3.registry import TrainerRegistry
from strategy_factory_trainers_v3.orchestrator import TaskOrchestrator
from strategy_factory_classical_v3 import register_classical_trainers,BY_ID
def run(a,h=None):
 s,rows,p=build_case(TaskKind.BINARY_CLASSIFICATION);r=TrainerRegistry();register_classical_trainers(r);d=BY_ID[a];p=replace(p,trainer=replace(p.trainer,trainer_id=d.trainer_id,trainer_version=d.trainer_version,hyperparameters=h or d.default_hyperparameters));return TaskOrchestrator(r).run(p,s,rows)
def test_constant_baselines():
 a=run('never_trade');b=run('always_trade');assert {x.outputs[0] for x in a.final_test_predictions.records}=={0.0};assert {x.outputs[0] for x in b.final_test_predictions.records}=={1.0}
def test_prevalence_deterministic():assert run('prevalence').oof_predictions.evidence_hash==run('prevalence').oof_predictions.evidence_hash
def test_manual_policy_exact():assert all(x.outputs[0] in (0.0,1.0) for x in run('manual_threshold',{'feature_index':0,'threshold':0.0,'direction':1}).final_test_predictions.records)
def test_single_feature_search_serializes():assert run('single_feature_search').artifact_manifest.state_hash
def test_rate_matched_null_seeded():assert run('rate_matched_null').final_test_predictions.evidence_hash==run('rate_matched_null').final_test_predictions.evidence_hash
