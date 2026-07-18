from __future__ import annotations
from .canonical import with_digest
from .errors import BudgetError
def validate_budget(profile:dict,request:dict)->dict:
    if profile.get('wall_clock_budget_seconds')!=3600: raise BudgetError('ACL13_ONE_HOUR_BUDGET_REQUIRED')
    if len(request['observations'])>profile['max_observations']: raise BudgetError('ACL13_OBSERVATION_BUDGET_EXCEEDED')
    if len(request['declared_setup_families'])>profile['max_setup_families']: raise BudgetError('ACL13_SETUP_FAMILY_BUDGET_EXCEEDED')
    if any(profile.get(k) is not False for k in ['network_access_allowed','gpu_required','budget_expansion_allowed']): raise BudgetError('ACL13_BUDGET_CAPABILITY_INVALID')
    return with_digest({'schema_version':'1.0.0','profile_id':profile['profile_id'],'wall_clock_budget_seconds':profile['wall_clock_budget_seconds'],'max_observations':profile['max_observations'],'max_setup_families':profile['max_setup_families'],'max_random_trials':profile['max_random_trials'],'request_observation_count':len(request['observations']),'request_setup_family_count':len(request['declared_setup_families']),'within_budget':True},'budget_validation_digest')
def usage_report(profile:dict,request:dict,random_trials:int)->dict:
    obs=len(request['observations']); fam=len(request['declared_setup_families'])
    charged_cpu_seconds=round(1.5+obs*0.02+fam*0.15+random_trials*0.005,3)
    body={'schema_version':'1.0.0','profile_id':profile['profile_id'],'wall_clock_budget_seconds':profile['wall_clock_budget_seconds'],'charged_cpu_seconds':charged_cpu_seconds,'peak_memory_mb':64,'observations_processed':obs,'setup_families_evaluated':fam,'random_trials_executed':random_trials,'network_calls':0,'gpu_calls':0,'budget_breached':False,'budget_expansion_used':False}
    return with_digest(body,'budget_usage_digest')
