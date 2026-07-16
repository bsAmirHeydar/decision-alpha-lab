from __future__ import annotations
from .canonical import content_hash

def score(rule_count,predicate_count,temporal_count,counterexample_count,fidelity):
    complexity=rule_count+0.5*predicate_count+1.5*temporal_count
    error=counterexample_count+100.0*(1.0-float(fidelity));total=complexity+error
    return {'rule_count':rule_count,'predicate_count':predicate_count,'temporal_count':temporal_count,'counterexample_count':counterexample_count,'fidelity':fidelity,'complexity_cost':complexity,'error_cost':error,'total_mdl_cost':total,'score_hash':content_hash([rule_count,predicate_count,temporal_count,counterexample_count,fidelity])}
