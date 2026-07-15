from __future__ import annotations
from collections import defaultdict
from statistics import mean
from .canonical import content_hash, stable_id
from .errors import EvaluationError

def _q(values:list[float],q:float)->float:
    if not values:return 0.0
    xs=sorted(values); pos=(len(xs)-1)*q; lo=int(pos); hi=min(lo+1,len(xs)-1); w=pos-lo
    return xs[lo]*(1-w)+xs[hi]*w

def evaluate_registry(registry:dict,twin:dict)->dict:
    by_node=defaultdict(list)
    for row in twin['rows']: by_node[row['node_id']].append(row)
    results=[]
    for entry in registry['entries']:
        rows=by_node.get(entry['projected_node_id'],[])
        if not rows: raise EvaluationError(f"no execution-twin rows for {entry['projected_node_id']}")
        order_rows=[r for r in rows if r['action_class']=='ordinary']
        values=[float(r['adjusted_net_r']) for r in order_rows]
        costs=[float(r['incremental_execution_cost_r']) for r in order_rows]
        fills=[float(r['fill_fraction']) for r in order_rows]
        scenarios=sorted({r['scenario_id'] for r in rows})
        per=[]
        for sid in scenarios:
            rr=[r for r in rows if r['scenario_id']==sid]
            oo=[r for r in rr if r['action_class']=='ordinary']
            per.append({"scenario_id":sid,"row_count":len(rr),"mean_adjusted_net_r":mean([float(r['adjusted_net_r']) for r in oo]) if oo else 0.0,"mean_fill_fraction":mean([float(r['fill_fraction']) for r in oo]) if oo else 0.0,"rejection_rate":sum(r['status']=='rejected' for r in oo)/len(oo) if oo else 0.0})
        results.append({"baseline_key":entry['baseline_key'],"projected_node_id":entry['projected_node_id'],"row_count":len(rows),"scenario_count":len(scenarios),"mean_adjusted_net_r":mean(values) if values else 0.0,"median_adjusted_net_r":_q(values,.5),"p10_adjusted_net_r":_q(values,.1),"worst_adjusted_net_r":min(values) if values else 0.0,"mean_incremental_cost_r":mean(costs) if costs else 0.0,"mean_fill_fraction":mean(fills) if fills else 0.0,"scenario_metrics":per,"benchmark_semantics":"descriptive_offline_reference_only"})
    payload={"phase":"SAED_V4_10","source_twin_id":twin['twin_id'],"source_twin_hash":twin['twin_hash'],"source_evidence_class":twin['evidence_class'],"synthetic_watermark":bool(twin['synthetic_watermark']),"results":results,"baseline_count":len(results),"ranking_semantics":"none","promotion_evidence":False,"selection_authority":False,"execution_authority":False,"limitations":["Metrics describe frozen reference baselines on the V4-09 synthetic execution twin.","No ordering, winner, recommendation, alpha or promotion claim is emitted."]}
    payload['benchmark_id']=stable_id('baselinebenchmark',payload);payload['benchmark_hash']=content_hash(payload)
    return payload
