from __future__ import annotations
import math
from .numerics import mean_vec,weighted_mean,l2,softmax,clamp
from .canonical import content_hash,stable_id

def _dispersion(vs,center): return sum(l2(v,center) for v in vs)/max(1,len(vs))
def _weights(candidate,views):
    vs=[x['embedding'] for x in views]
    if candidate.algorithm=='late_mean_baseline': return [1.0]*len(views)
    if candidate.algorithm=='quality_gated': return [max(1e-9,x['quality'])*math.exp(-x['age_seconds']/86400.0) for x in views]
    center=mean_vec(vs)
    if candidate.algorithm=='masked_cross_attention_reference':
        scores=[sum(a*b for a,b in zip(x['embedding'],center))/math.sqrt(len(center))+math.log(max(x['quality'],1e-9)) for x in views]
        return list(softmax(scores))
    if candidate.algorithm=='evidential_product_of_experts':
        return [max(1e-9,x['quality'])/(float(x.get('uncertainty',1.0))**2+1e-6) for x in views]
    if candidate.algorithm=='disagreement_aware_mixture':
        return [max(1e-9,x['quality'])/(1.0+l2(x['embedding'],center)) for x in views]
    raise ValueError('unknown fusion algorithm')

def fuse(candidate,envelopes,support,config):
    available=[x for x in envelopes if x['available']]
    if not support['supported']:
        doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'algorithm':candidate.algorithm,'status':'unsupported','directive':support['action'],'reasons':support['reasons'],'fused_embedding':[0.0]*config.common_dim,'view_weights':[],'uncertainty':1.0,'disagreement':0.0,'gate_concentration':0.0,'view_collapse':False,'known_as_of':max((x['known_as_of'] for x in envelopes),default=''),'production_eligible':False}
    else:
        raw=_weights(candidate,available);s=sum(raw);weights=[w/s for w in raw];center=weighted_mean([x['embedding'] for x in available],weights);disp=_dispersion([x['embedding'] for x in available],center);conc=max(weights);collapse=conc>config.max_gate_concentration
        uncertainty=clamp((sum(float(x.get('uncertainty',1.0))*w for x,w in zip(available,weights))+disp)* (config.uncertainty_inflation if disp>config.disagreement_threshold else 1.0),0.0,10.0)
        directive='baseline' if collapse and candidate.algorithm!='late_mean_baseline' else 'fuse'
        doc={'phase':'SAED_V4_15','candidate_id':candidate.candidate_id,'algorithm':candidate.algorithm,'status':'supported','directive':directive,'reasons':['view_collapse'] if collapse else [],'fused_embedding':list(center),'view_weights':[{'view_name':x['view_name'],'source_plane':x['source_plane'],'weight':w} for x,w in zip(available,weights)],'uncertainty':uncertainty,'disagreement':disp,'gate_concentration':conc,'view_collapse':collapse,'known_as_of':max(x['known_as_of'] for x in available),'production_eligible':False}
    doc['fusion_hash']=content_hash(doc);doc['fusion_id']=stable_id('v415fusion',doc);return doc
