from .canonical import content_hash,stable_id

def make(candidate,output,metric,support,aligned):
    doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'algorithm':candidate.algorithm,'fusion_hash':output['fusion_hash'],'aligned_set_hash':aligned['aligned_set_hash'],'support_audit_hash':support['audit_hash'],'reference_score':metric['reference_score'],'status':'research_checkpoint','runtime_eligible':False,'production_eligible':False,'revoked':False};doc['checkpoint_hash']=content_hash(doc);doc['checkpoint_id']=stable_id('v415checkpoint',doc);return doc
