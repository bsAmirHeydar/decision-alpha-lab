from __future__ import annotations
from .canonical import content_hash

def candidate_metrics(candidates,baseline_graph,temporal_graph,truth,invariance,negative_controls,graph_metric_fn):
    rows=[]
    for c in candidates:
        if not c.enabled:continue
        graph=baseline_graph if c.algorithm=='correlation_baseline' else temporal_graph
        gm=graph_metric_fn(graph,truth);inv_rate=invariance['invariant_count']/max(1,invariance['mechanism_count']);neg=1.0 if negative_controls['all_passed'] else 0.0;complexity=len(graph['edges'])/max(1,len(graph['nodes'])**2)
        score=0.46*gm['f1']+0.28*inv_rate+0.18*neg-0.08*c.edge_penalty*complexity-0.01*c.complexity_tier
        rows.append({'candidate_id':c.candidate_id,'algorithm':c.algorithm,'complexity_tier':c.complexity_tier,'graph_hash':graph['graph_hash'],'edge_count':len(graph['edges']),**gm,'invariance_rate':inv_rate,'negative_control_pass_rate':neg,'reference_score':score,'causal_claim_allowed':False,'production_eligible':False})
    out={'phase':'SAED_V4_17','row_count':len(rows),'rows':rows};out['report_hash']=content_hash(out);return out

def select(metrics):
    rows=sorted(metrics['rows'],key=lambda r:(-r['reference_score'],r['complexity_tier'],r['candidate_id']));baseline=next(r for r in rows if r['algorithm']=='correlation_baseline');champ=rows[0]
    out={'phase':'SAED_V4_17','candidate_count':len(rows),'ranking':[r['candidate_id'] for r in rows],'reference_champion_id':champ['candidate_id'],'reference_champion_score':champ['reference_score'],'baseline_candidate_id':baseline['candidate_id'],'baseline_score':baseline['reference_score'],'baseline_preserved':True,'champion_is_research_only':True,'causal_claim_authority':False,'production_authority':False};out['tournament_hash']=content_hash(out);return out
