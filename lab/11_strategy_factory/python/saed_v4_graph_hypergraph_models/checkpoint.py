from .canonical import content_hash,stable_id
def make_checkpoint(candidate,encoded,evaluation,graph):
    body={'phase':'SAED_V4_13','candidate_id':candidate.candidate_id,'architecture':candidate.architecture,'seed':candidate.seed,'hidden_dim':candidate.hidden_dim,'output_dim':candidate.output_dim,'layers':candidate.layers,'compiled_graph_hash':graph['compiled_graph_hash'],'embedding_hash':encoded['embedding_hash'],'evaluation_hash':evaluation['evaluation_hash'],'composite_score':evaluation['composite_score'],'production_eligible':False,'runtime_authority':False}
    body['checkpoint_hash']=content_hash(body);body['checkpoint_id']=stable_id('graphckpt',body);return body
