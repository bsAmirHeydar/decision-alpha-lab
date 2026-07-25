from .canonical import content_hash,stable_id
from .errors import BudgetError

def enforce(seq,candidates,budget,decisions):
    enabled=[c for c in candidates if c.enabled]; admitted={d['intake_id'] for d in decisions if d['decision']=='admit_reference'};active=[c for c in enabled if c.intake_id in admitted]
    calls=len(active);tokens=calls*len(seq['tokens']);params=sum(c.trainable_parameter_budget for c in active);exposures=calls*3
    checks={'candidate_budget':len(active)<=budget.max_candidates,'adapter_call_budget':calls<=budget.max_adapter_calls,'token_budget':tokens<=budget.max_total_tokens,'trainable_parameter_budget':params<=budget.max_trainable_parameters,'exposure_budget':exposures<=budget.max_exposure_events}
    if not all(checks.values()):raise BudgetError(f'compute/exposure budget exceeded: {checks}')
    doc={'phase':'SAED_V4_14','active_candidate_count':len(active),'adapter_calls':calls,'total_tokens':tokens,'trainable_parameters':params,'exposure_events':exposures,'failure_count':0,'retry_count':0,'checks':checks,'complete_accounting':True}
    doc['ledger_hash']=content_hash(doc);doc['ledger_id']=stable_id('fmbudget',doc);return doc
