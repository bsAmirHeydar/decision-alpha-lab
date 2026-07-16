from .errors import BudgetError
from .canonical import content_hash

def enforce(budget,dataset,variables,candidates,conditional_tests,bootstrap_replicates,stress_runs):
    usage={'rows':dataset['row_count'],'variables':len(variables.variables),'candidates':len(candidates),'edges_evaluated':len(variables.variables)**2,'conditional_tests':conditional_tests,'bootstrap_replicates':bootstrap_replicates,'stress_runs':stress_runs,'failures':0,'retries':0,'protected_evidence_exposures':dataset['protected_evidence_exposures'],'hidden_evaluation_queries':0}
    limits={'rows':budget.max_rows,'variables':budget.max_variables,'candidates':budget.max_candidates,'edges_evaluated':budget.max_edges_evaluated,'conditional_tests':budget.max_conditional_tests,'bootstrap_replicates':budget.max_bootstrap_replicates,'stress_runs':budget.max_stress_runs,'failures':budget.max_failures,'retries':budget.max_retries,'protected_evidence_exposures':budget.protected_evidence_exposure_limit,'hidden_evaluation_queries':budget.hidden_evaluation_query_limit}
    exceeded=[k for k in usage if usage[k]>limits[k]]
    if exceeded:raise BudgetError('budget exceeded: '+','.join(exceeded))
    out={'phase':'SAED_V4_17','usage':usage,'limits':limits,'exceeded':exceeded,'passed':not exceeded};out['ledger_hash']=content_hash(out);return out
