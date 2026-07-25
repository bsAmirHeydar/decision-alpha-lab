from __future__ import annotations
from .contracts import *
from .ledger import TournamentLedger
from .evaluation import deterministic_trial_metrics,aggregate_metrics
from .enums import TrialStatus,Stage
from .canonical import canonical_sha256,stable_id
from .errors import TournamentError

def declared_trial_count(context_ids,treatments,algorithms,folds):return len(context_ids)*len(treatments)*len(algorithms)*len(folds)

def run_reference_tournament(freeze:TournamentFreeze,context_ids:tuple[str,...],treatments:TreatmentUniverseFreeze,algorithms:AlgorithmUniverseFreeze,ledger:TournamentLedger|None=None,fail_trial_ids:set[str]|None=None)->TournamentReport:
 ledger=ledger or TournamentLedger();fail_trial_ids=fail_trial_ids or set();results=[];declared=declared_trial_count(context_ids,treatments.treatments,algorithms.algorithms,freeze.folds)
 ledger.append(Stage.FREEZE,'tournament_frozen',{'freeze_hash':freeze.freeze_hash,'declared':declared},0)
 budget=freeze.budget_units;used=0
 for c in sorted(context_ids):
  for t in sorted(treatments.treatments,key=lambda x:x.treatment_id):
   for a in sorted(algorithms.algorithms,key=lambda x:x.algorithm_id):
    for f in sorted(freeze.folds,key=lambda x:x.fold_id):
     trial_id=stable_id('uce15_trial',{'c':c,'t':t.treatment_id,'a':a.algorithm_id,'f':f.fold_id,'freeze':freeze.freeze_hash})
     if used+a.budget_units>budget:
      r=TrialResult(trial_id,c,t.treatment_id,a.algorithm_id,f.fold_id,TrialStatus.SKIPPED,{},0,'budget_exhausted',canonical_sha256({'trial':trial_id,'status':'skipped'}));results.append(r);continue
     used+=a.budget_units
     if trial_id in fail_trial_ids:
      r=TrialResult(trial_id,c,t.treatment_id,a.algorithm_id,f.fold_id,TrialStatus.FAILED,{},0,'injected_failure',canonical_sha256({'trial':trial_id,'status':'failed'}))
     else:
      metrics=deterministic_trial_metrics(c,t.treatment_id,a.algorithm_id,f.fold_id,a.seed)
      r=TrialResult(trial_id,c,t.treatment_id,a.algorithm_id,f.fold_id,TrialStatus.SUCCEEDED,metrics,24,'none',canonical_sha256({'trial':trial_id,'metrics':metrics}))
     results.append(r);ledger.append(Stage.TOURNAMENT,'trial_completed',{'trial_id':trial_id,'status':r.status.value,'hash':r.result_hash},used)
 succeeded=sum(r.status is TrialStatus.SUCCEEDED for r in results);failed=sum(r.status is TrialStatus.FAILED for r in results);executed=succeeded+failed
 ranked=[]
 groups={}
 for r in results:
  if r.status is TrialStatus.SUCCEEDED:groups.setdefault((r.context_id,r.treatment_id,r.algorithm_id),[]).append(r.metrics)
 for key,rows in groups.items():
  agg=aggregate_metrics(rows);score=agg.get('sharpe',-999)-2*agg.get('calibration_error',0)+0.1*agg.get('mean_net_r',0);ranked.append((score,key))
 ranked.sort(key=lambda x:(-x[0],x[1]));candidates=tuple(stable_id('uce15_candidate',{'context_id':k[0],'treatment_id':k[1],'algorithm_id':k[2]}) for _,k in ranked[:freeze.max_challengers])
 findings=[]
 if any(r.status is TrialStatus.SKIPPED for r in results):findings.append('budget_exhausted_trials_present')
 report=TournamentReport(stable_id('uce15_tournament_report',{'freeze':freeze.freeze_hash,'tail':ledger.tail_hash}), '1.0.0',freeze.freeze_hash,tuple(results),ledger.tail_hash,declared,executed,succeeded,failed,candidates,tuple(findings),True)
 ledger.append(Stage.TOURNAMENT,'tournament_reported',{'report_hash':report.report_hash},used+1)
 return report
