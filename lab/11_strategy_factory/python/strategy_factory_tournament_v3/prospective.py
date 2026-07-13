from __future__ import annotations
from .contracts import *
from .enums import DataMode,ReconciliationStatus
from .canonical import stable_id
from .errors import TournamentError

def reconcile_observation(plan:ProspectivePaperPlan,obs:PaperObservation)->tuple[ReconciliationStatus,tuple[str,...]]:
 if obs.observed_entry is None or obs.observed_cost is None:return ReconciliationStatus.MISSING,('missing_observed_fill_or_cost',)
 diffs=(abs(obs.expected_entry-obs.observed_entry),abs(obs.expected_cost-obs.observed_cost))
 if max(diffs)>plan.reconciliation_tolerance:return ReconciliationStatus.MISMATCH,('reconciliation_tolerance_exceeded',)
 return ReconciliationStatus.MATCH,()

def build_paper_report(plan:ProspectivePaperPlan,observations:tuple[PaperObservation,...],mode:DataMode,completed:bool,untouched:bool=True)->ProspectivePaperReport:
 seen=set();matched=0;mismatch=0;findings=[]
 for o in observations:
  if o.decision_hash in seen:findings.append('duplicate_decision_hash');mismatch+=1;continue
  seen.add(o.decision_hash)
  status,reasons=reconcile_observation(plan,o)
  if status is ReconciliationStatus.MATCH:matched+=1
  else:mismatch+=1;findings.extend(reasons)
 if len(observations)<plan.minimum_decisions:findings.append('insufficient_prospective_decisions')
 if mode is not DataMode.PROSPECTIVE_PAPER:findings.append('not_prospective_paper_data')
 if not completed:findings.append('prospective_window_incomplete')
 drift=mismatch/max(1,len(observations))
 return ProspectivePaperReport(stable_id('uce15_paper_report',{'plan':plan.plan_hash,'obs':[o.observation_id for o in observations]}),'1.0.0',plan.plan_hash,mode,observations,len(observations),matched,mismatch,drift,untouched,completed,tuple(dict.fromkeys(findings)))
