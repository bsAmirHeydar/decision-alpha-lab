from .canonical import content_hash,stable_id

def run(metrics,baseline_id):
    rows=sorted(metrics['rows'],key=lambda x:(-x['reference_score'],x['candidate_id']));champion=rows[0]['candidate_id'];baseline=next(x for x in rows if x['candidate_id']==baseline_id)
    doc={'phase':'SAED_V4_15','baseline_candidate_id':baseline_id,'baseline_preserved':True,'reference_champion_id':champion,'ranking':[x['candidate_id'] for x in rows],'rows':rows,'promotion_authority':False,'economic_promotion':False,'production_eligible':False};doc['tournament_hash']=content_hash(doc);doc['tournament_id']=stable_id('v415tournament',doc);return doc
