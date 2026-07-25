from __future__ import annotations
from .errors import BudgetError
from .canonical import content_hash

def enforce(budget,dataset,treatments,estimators,policies,folds,bootstrap_replicates,sensitivity_runs):
    usage={'rows':dataset['row_count'],'treatments':len(treatments.treatments),'estimators':len(estimators),'policies':len(policies),'cross_fit_folds':folds,'bootstrap_replicates':bootstrap_replicates,'sensitivity_runs':sensitivity_runs,'failures':0,'retries':0,'protected_evidence_exposures':dataset['protected_evidence_exposures'],'hidden_evaluation_queries':0}
    limits={'rows':budget.max_rows,'treatments':budget.max_treatments,'estimators':budget.max_estimators,'policies':budget.max_policies,'cross_fit_folds':budget.max_cross_fit_folds,'bootstrap_replicates':budget.max_bootstrap_replicates,'sensitivity_runs':budget.max_sensitivity_runs,'failures':budget.max_failures,'retries':budget.max_retries,'protected_evidence_exposures':budget.protected_evidence_exposure_limit,'hidden_evaluation_queries':budget.hidden_evaluation_query_limit}
    exceeded={k:usage[k]>limits[k] for k in usage}
    if any(exceeded.values()):raise BudgetError(f'budget exceeded: {[k for k,v in exceeded.items() if v]}')
    out={'phase':'SAED_V4_18','usage':usage,'limits':limits,'exceeded':exceeded,'passed':True};out['ledger_hash']=content_hash(out);return out
