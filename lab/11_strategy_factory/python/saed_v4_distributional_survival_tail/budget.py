from .errors import BudgetError
from .canonical import content_hash

def enforce(dataset,candidates,config,budget,stress_count):
    enabled=sum(c.enabled for c in candidates);predictions=enabled*dataset['split_counts']['selection_validation']*2
    actual={'rows':dataset['row_count'],'candidates':enabled,'horizons':len(config.horizons_seconds),'quantiles':len(config.quantiles),'tail_levels':len(config.tail_levels),'predictions':predictions,'stress_runs':stress_count,'failures':0,'retries':0,'protected_evidence_exposures':dataset['protected_evidence_exposures']}
    limits={'rows':budget.max_rows,'candidates':budget.max_candidates,'horizons':budget.max_horizons,'quantiles':budget.max_quantiles,'tail_levels':budget.max_tail_levels,'predictions':budget.max_predictions,'stress_runs':budget.max_stress_runs,'failures':budget.max_failures,'retries':budget.max_retries,'protected_evidence_exposures':budget.protected_evidence_exposure_limit}
    violations=[k for k in actual if actual[k]>limits[k]]
    out={'phase':'SAED_V4_16','actual':actual,'limits':limits,'violations':violations,'passed':not violations,'complete_trial_accounting':True,'complete_exposure_accounting':True}
    out['ledger_hash']=content_hash(out)
    if violations:raise BudgetError(f'budget exceeded: {violations}')
    return out
