from dataclasses import asdict,replace
from time import perf_counter
import tracemalloc
from strategy_factory_trainers_v3.orchestrator import TaskOrchestrator
from strategy_factory_trainers_v3.registry import TrainerRegistry
from strategy_factory_trainers_v3.canonical import canonical_sha256,stable_id
from strategy_factory_trainers_v3.enums import CalibrationKind
from .contracts import *
from .catalog import BY_ID
from .registry import register_classical_trainers
from .dependency import DependencyProbe
class BenchmarkRunner:
 def __init__(self,probe=None):self.probe=probe or DependencyProbe()
 def run_case(self,case,plan,schema,rows,algorithm_id):
  d=BY_ID[algorithm_id];a=self.probe.evaluate(d)
  if not a.available:return BenchmarkObservation(stable_id('ucebenchobs',{'case':case.case_id,'alg':d.key}),case.case_id,d.key,d.family,BenchmarkStatus.SKIPPED_UNAVAILABLE,plan.task.primary_metric,0.0,'unavailable',0.0,0,0,0.0,False,False,False,False,'','','dependency_unavailable',a.reason)
  r=TrainerRegistry();register_classical_trainers(r,probe=self.probe);o=TaskOrchestrator(r);cfg=replace(plan.trainer,trainer_id=d.trainer_id,trainer_version=d.trainer_version,hyperparameters=d.default_hyperparameters,calibration_kind=CalibrationKind.IDENTITY if d.probability_output else CalibrationKind.NONE);pp=replace(plan,trainer=cfg)
  try:
   tracemalloc.start();t=perf_counter();x=o.run(pp,schema,rows,'uce_i08_benchmark');fit=int((perf_counter()-t)*1000);_,peak=tracemalloc.get_traced_memory();tracemalloc.stop();t=perf_counter();y=o.run(pp,schema,rows,'uce_i08_benchmark');repeat=int((perf_counter()-t)*1000);metric=float(x.final_trial.metrics.get(plan.task.primary_metric,0.0));det=x.oof_predictions.evidence_hash==y.oof_predictions.evidence_hash and x.final_test_predictions.evidence_hash==y.final_test_predictions.evidence_hash;cal='identity' if d.probability_output else 'not_applicable';return BenchmarkObservation(stable_id('ucebenchobs',{'case':case.case_id,'alg':d.key,'oof':x.oof_predictions.evidence_hash}),case.case_id,d.key,d.family,BenchmarkStatus.SUCCEEDED,plan.task.primary_metric,metric,cal,0.0,fit,repeat,peak/1048576,det,True,'onnx' in d.export_formats,True,x.oof_predictions.evidence_hash,x.final_test_predictions.evidence_hash,warnings=d.limitations)
  except Exception as e:
   try:tracemalloc.stop()
   except Exception:pass
   return BenchmarkObservation(stable_id('ucebenchobs',{'case':case.case_id,'alg':d.key,'error':type(e).__name__}),case.case_id,d.key,d.family,BenchmarkStatus.FAILED,plan.task.primary_metric,0.0,'failed',0.0,0,0,0.0,False,False,False,False,'','',type(e).__name__,str(e))
 def report(self,plan_id,cases_and_data,algorithm_ids,required=(AlgorithmFamily.BASELINE,AlgorithmFamily.LINEAR,AlgorithmFamily.TREE)):
  obs=[]
  for case,plan,schema,rows in cases_and_data:
   for aid in algorithm_ids:obs.append(self.run_case(case,plan,schema,rows,aid))
  present={x.family for x in obs if x.status is BenchmarkStatus.SUCCEEDED};missing=tuple(x for x in required if x not in present);prob_ok=all(x.calibration_metric in ('identity','not_applicable','unavailable') or x.status is not BenchmarkStatus.SUCCEEDED for x in obs);optional_ok=all(x.status in (BenchmarkStatus.SUCCEEDED,BenchmarkStatus.SKIPPED_UNAVAILABLE) or x.family is not AlgorithmFamily.OPTIONAL_EXTERNAL for x in obs);h=canonical_sha256({'plan':plan_id,'obs':[asdict(x) for x in obs],'missing':[x.value for x in missing]});return BenchmarkReport(stable_id('ucebench',h),plan_id,tuple(obs),tuple(required),missing,prob_ok,optional_ok,not missing and prob_ok and optional_ok,h)
class ClassicalGateEvaluator:
 @staticmethod
 def evaluate(context_id,report):
  present=tuple(sorted({x.family for x in report.observations if x.status is BenchmarkStatus.SUCCEEDED},key=lambda x:x.value));block=[];warn=[]
  if report.missing_required_families:block.append('missing_required_classical_family')
  if not report.all_probability_disclosed:block.append('probability_calibration_undisclosed')
  if not report.all_optional_failures_clean:block.append('optional_dependency_failure_not_clean')
  if any(not x.deterministic_rerun for x in report.observations if x.status is BenchmarkStatus.SUCCEEDED):warn.append('numeric_rerun_drift')
  state=ComparisonGateState.BLOCK if block else(ComparisonGateState.REVIEW if warn else ComparisonGateState.PASS);h=canonical_sha256({'context':context_id,'report':report.report_id,'block':block,'warn':warn});return ClassicalComparisonGate(stable_id('uceclassgate',h),context_id,report.report_id,state,report.required_families,present,tuple(block),tuple(warn),h)
