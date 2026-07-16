from __future__ import annotations
from .numerics import l2,mean_vec
from .canonical import content_hash,stable_id

def disagreement(outputs):
    rows=[]
    for o in outputs:
        rows.append({'candidate_id':o['candidate_id'],'disagreement':o['disagreement'],'uncertainty':o['uncertainty'],'gate_concentration':o['gate_concentration'],'view_collapse':o['view_collapse'],'calibrated_direction':'uncertainty_non_decreasing_with_disagreement'})
    doc={'phase':'SAED_V4_15','rows':rows,'row_count':len(rows),'attention_is_causal':False,'production_eligible':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('v415disagreement',doc);return doc

def ablation(candidate,envelopes,base_output,config,support_fn,fuse_fn):
    rows=[]
    for e in envelopes:
        mutated=[dict(x,available=False) if x['view_name']==e['view_name'] else x for x in envelopes];sup=support_fn(mutated);out=fuse_fn(mutated,sup)
        drift=l2(base_output['fused_embedding'],out['fused_embedding']) if out['status']=='supported' else -1.0
        rows.append({'view_name':e['view_name'],'source_plane':e['source_plane'],'directive':out['directive'],'supported':out['status']=='supported','embedding_drift':drift,'causal_claim':False})
    doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'rows':rows,'row_count':len(rows),'diagnostic_only':True,'production_eligible':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('v415ablation',doc);return doc

def attribution(outputs):
    rows=[]
    for o in outputs:
        for w in o['view_weights']:rows.append({'candidate_id':o['candidate_id'],'view_name':w['view_name'],'source_plane':w['source_plane'],'diagnostic_weight':w['weight'],'causal_interpretation_permitted':False})
    doc={'phase':'SAED_V4_15','rows':rows,'row_count':len(rows),'attention_or_gate_weights_are_not_causal':True,'production_eligible':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('v415attribution',doc);return doc

def permutation(candidate,envelopes,support,fuse_fn):
    a=fuse_fn(envelopes,support);b=fuse_fn(list(reversed(envelopes)),support);same=a['fused_embedding']==b['fused_embedding'] and sorted(a['view_weights'],key=lambda x:x['view_name'])==sorted(b['view_weights'],key=lambda x:x['view_name'])
    doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'permutation_invariant':same,'original_fusion_hash':a['fusion_hash'],'reversed_fusion_hash':b['fusion_hash'],'production_eligible':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('v415permutation',doc);return doc
