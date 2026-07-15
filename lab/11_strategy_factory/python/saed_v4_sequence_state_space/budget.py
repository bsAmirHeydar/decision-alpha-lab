from .canonical import content_hash,stable_id
from .errors import BudgetError

def compute_budget(candidate_count,max_pairs,max_state_dim,max_context_steps,max_wall_seconds):
    if min(candidate_count,max_pairs,max_state_dim,max_context_steps,max_wall_seconds)<1:raise BudgetError('invalid compute budget')
    material={'candidate_count_limit':candidate_count,'training_pair_limit':max_pairs,'state_dim_limit':max_state_dim,'context_step_limit':max_context_steps,'wall_clock_seconds_limit':max_wall_seconds,'gpu_hours':0.0,'distributed_workers':1,'retry_limit':0}
    return {**material,'budget_id':stable_id('seqbudget',material),'budget_hash':content_hash(material)}
