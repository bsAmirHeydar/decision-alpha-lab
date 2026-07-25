from .canonical import content_hash,stable_id

def run(metrics,baseline_id):
    rows=sorted(metrics,key=lambda x:(-x['composite_score'],x['candidate_id']));base=next(x for x in rows if x['candidate_id']==baseline_id);champ=rows[0]
    ranking=[{'rank':i+1,'candidate_id':r['candidate_id'],'family':r['family'],'adapter_mode':r['adapter_mode'],'composite_score':r['composite_score']} for i,r in enumerate(rows)]
    doc={'phase':'SAED_V4_14','ranking':ranking,'reference_champion_id':champ['candidate_id'],'baseline_id':baseline_id,'baseline_score':base['composite_score'],'baseline_preserved':True,'selection_scope':'synthetic_reference_self_supervised_only','economic_uplift_evaluated':False,'production_authority':False}
    doc['tournament_hash']=content_hash(doc);doc['tournament_id']=stable_id('fmtournament',doc);return doc
