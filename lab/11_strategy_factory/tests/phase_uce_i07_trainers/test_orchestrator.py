from strategy_factory_trainers_v3 import *
from strategy_factory_trainers_v3.golden import build_case
def run(task):
 r=TrainerRegistry();register_reference_trainers(r);s,rows,p=build_case(task);return TaskOrchestrator(r).run(p,s,rows,'test'),s,p
def test_all_three_task_families():
 for t in (TaskKind.BINARY_CLASSIFICATION,TaskKind.REGRESSION,TaskKind.RANKING):
  x,s,p=run(t);assert x.final_trial.status is TrialStatus.SUCCEEDED;assert len(x.oof_predictions.records)==4 and len(x.final_test_predictions.records)==4;assert x.artifact_manifest.feature_order==s.feature_order
def test_binary_threshold_and_lineage():
 x,s,p=run(TaskKind.BINARY_CLASSIFICATION);assert x.threshold is not None and all(r.predicted_class in (0,1) for r in x.final_test_predictions.records);assert all(r.lineage.role is SplitRole.FINAL_TEST for r in x.final_test_predictions.records)
def test_deterministic_rerun():
 a,_,_=run(TaskKind.RANKING);b,_,_=run(TaskKind.RANKING);assert a.oof_predictions.evidence_hash==b.oof_predictions.evidence_hash and a.final_test_predictions.evidence_hash==b.final_test_predictions.evidence_hash
