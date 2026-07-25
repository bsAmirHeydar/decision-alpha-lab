from .canonical import content_hash,stable_id

def run(metrics,baseline_id):
    rows=sorted(metrics['rows'],key=lambda x:(-x['reference_score'],x['candidate_id']));champion=rows[0]['candidate_id'];baseline=next(x for x in rows if x['candidate_id']==baseline_id)
    out={'phase':'SAED_V4_16','tournament_id':stable_id('v416tournament',rows),'baseline_candidate_id':baseline_id,'baseline_preserved':True,'reference_champion_id':champion,'reference_champion_score':rows[0]['reference_score'],'baseline_score':baseline['reference_score'],'candidate_count':len(rows),'ranking':[{'rank':i+1,'candidate_id':r['candidate_id'],'algorithm':r['algorithm'],'reference_score':r['reference_score']} for i,r in enumerate(rows)],'synthetic_reference_only':True,'promotion_decision':'not_in_scope','production_authority':False};out['tournament_hash']=content_hash(out);return out
