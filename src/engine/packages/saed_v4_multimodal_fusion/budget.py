from .errors import BudgetError
from .canonical import content_hash,stable_id

def enforce(candidates,domain_matrix,foundation_matrix,dropout_plan,aligned,budget):
    usage={'candidates':len(candidates),'fusion_calls':len(candidates),'domain_subset_evaluations':domain_matrix['subset_count'],'foundation_subset_evaluations':foundation_matrix['subset_count'],'dropout_patterns':dropout_plan['pattern_count'],'total_vector_dimensions':(aligned['domain_view_count']+aligned['foundation_view_count'])*aligned['common_dim'],'failures':0,'retries':0}
    limits={'candidates':budget.max_candidates,'fusion_calls':budget.max_fusion_calls,'domain_subset_evaluations':budget.max_domain_subset_evaluations,'foundation_subset_evaluations':budget.max_foundation_subset_evaluations,'dropout_patterns':budget.max_dropout_patterns,'total_vector_dimensions':budget.max_total_vector_dimensions,'failures':budget.max_failures,'retries':budget.max_retries}
    breaches=[k for k in usage if usage[k]>limits[k]]
    if breaches:raise BudgetError('budget exceeded: '+','.join(breaches))
    doc={'phase':'SAED_V4_15','usage':usage,'limits':limits,'breaches':breaches,'passed':not breaches,'protected_evidence_exposures':0,'outcome_label_exposures':0,'production_eligible':False};doc['ledger_hash']=content_hash(doc);doc['ledger_id']=stable_id('v415ledger',doc);return doc
