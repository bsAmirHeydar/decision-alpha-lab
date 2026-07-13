from .contracts import TaskComparisonReport
from .canonical import canonical_sha256,stable_id
from .enums import GateDecision

def build_task_comparison(context_id,dataset_manifest_hash,observations,required_families):
 attempted=tuple(sorted({o.task_family for o in observations},key=lambda x:x.value));missing=tuple(x for x in required_families if x not in attempted);blockers=[];warnings=[];best={}
 for family in attempted:
  eligible=[o for o in observations if o.task_family is family and o.status=='succeeded' and o.support_gate is not GateDecision.REJECT]
  if eligible:best[family.value]=max(eligible,key=lambda x:(x.economic_utility,x.primary_value,x.algorithm_key)).algorithm_key
  else:blockers.append('no_eligible_result:'+family.value)
 if missing:blockers.extend('missing_family:'+x.value for x in missing)
 if any(not o.deterministic for o in observations):warnings.append('nondeterministic_observation_present')
 h=canonical_sha256({'context':context_id,'dataset':dataset_manifest_hash,'observations':observations,'required':required_families});return TaskComparisonReport(stable_id('ucetaskcmp',h),context_id,dataset_manifest_hash,tuple(observations),attempted,missing,best,not blockers,tuple(blockers),tuple(warnings),h)
