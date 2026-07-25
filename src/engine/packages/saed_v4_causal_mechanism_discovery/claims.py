from __future__ import annotations
from .canonical import content_hash

def tier(graph_metrics,invariance,negative_controls,temporal,acyclicity):
    failures=[]
    if not temporal['all_passed']:failures.append('temporal_precedence')
    if not acyclicity['passed']:failures.append('acyclicity')
    if not negative_controls['all_passed']:failures.append('negative_controls')
    if invariance['invariant_count']<max(1,invariance['mechanism_count']//2):failures.append('mechanism_invariance')
    if failures:claim='associational';directive='association_fallback'
    elif graph_metrics['f1']>=0.45:claim='mechanism_compatible_synthetic';directive='continue_reference'
    else:claim='associational';directive='baseline'
    out={'phase':'SAED_V4_17','claim_tier':claim,'directive':directive,'failures':failures,'synthetic_benchmark_f1':graph_metrics['f1'],'real_causal_claim':False,'production_eligible':False,'claim_ceiling':'mechanism_compatible_synthetic_not_causal'};out['report_hash']=content_hash(out);return out

def claim_ledger():
    return {'phase':'SAED_V4_17','claims':[{'claim':'closed causal-mechanism discovery contracts implemented','status':'supported_local_reference'},{'claim':'deterministic synthetic benchmark and replay implemented','status':'supported_local_reference'},{'claim':'temporal, invariance, negative-control and sensitivity audits implemented','status':'supported_local_reference'},{'claim':'real causal mechanism discovered','status':'not_claimed'},{'claim':'real treatment effect identified','status':'not_claimed'},{'claim':'economic uplift established','status':'not_claimed'},{'claim':'production authorization','status':'not_claimed'}]}
