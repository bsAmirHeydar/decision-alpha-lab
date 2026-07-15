from .contracts import CandidateSpec,GraphSpec
from .models import encode
from .canonical import content_hash
def run_vectors(graph,spec_doc,vectors):
    spec=GraphSpec.from_mapping(spec_doc);results=[]
    for v in vectors:
        c=CandidateSpec.from_mapping(v['candidate']);a=encode(graph,spec,c);b=encode(graph,spec,c)
        results.append({'vector_id':v['vector_id'],'candidate_id':c.candidate_id,'embedding_hash':a['embedding_hash'],'repeat_hash':b['embedding_hash'],'passed':a['embedding_hash']==b['embedding_hash'],'tolerance':v['tolerance']})
    return {'phase':'SAED_V4_13','count':len(results),'passed':all(x['passed'] for x in results),'results':results,'result_hash':content_hash(results)}
