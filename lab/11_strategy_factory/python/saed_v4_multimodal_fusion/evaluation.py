from .numerics import cosine
from .canonical import content_hash,stable_id

def evaluate(outputs,domain_matrix,foundation_matrix):
    rows=[];domain_rob=sum(r['supported'] for r in domain_matrix['rows'])/domain_matrix['subset_count'];foundation_rob=sum(r['challenger_supported'] for r in foundation_matrix['rows'])/foundation_matrix['subset_count']
    for o in outputs:
        emb=o['fused_embedding'];coherence=sum(abs(x) for x in emb)/max(1,len(emb));agreement=1/(1+o['disagreement']);calibration=1/(1+abs(o['uncertainty']-o['disagreement']));collapse_penalty=o['gate_concentration'] if o['view_collapse'] else 0.0
        score=0.34*agreement+0.22*calibration+0.18*domain_rob+0.14*foundation_rob+0.12*coherence-0.20*collapse_penalty
        rows.append({'candidate_id':o['candidate_id'],'algorithm':o['algorithm'],'supported':o['status']=='supported','agreement_score':agreement,'uncertainty_calibration_score':calibration,'domain_subset_robustness':domain_rob,'foundation_subset_robustness':foundation_rob,'embedding_coherence':coherence,'collapse_penalty':collapse_penalty,'reference_score':score if o['status']=='supported' else -1.0,'economic_metric':False,'outcome_metric':False,'production_eligible':False})
    doc={'phase':'SAED_V4_15','rows':rows,'row_count':len(rows),'synthetic_reference_only':True,'economic_uplift_established':False,'production_eligible':False};doc['report_hash']=content_hash(doc);doc['report_id']=stable_id('v415metrics',doc);return doc
