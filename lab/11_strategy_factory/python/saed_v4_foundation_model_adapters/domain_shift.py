from .canonical import content_hash,stable_id
from .numerics import mean,std,clamp

def assess(seq,features,candidate,policy):
    xs=[x for t in seq['tokens'] for x in t['feature']];half=max(1,len(seq['tokens'])//2);a=[x for t in seq['tokens'][:half] for x in t['feature']];b=[x for t in seq['tokens'][half:] for x in t['feature']]
    ma=sum(a)/len(a);mb=sum(b)/len(b);sa=std(a) or 1e-8;sb=std(b) or 1e-8;mean_shift=abs(mb-ma);scale_ratio=max(sa,sb)/min(sa,sb);missing=sum(sum(t['missing_mask']) for t in seq['tokens'])/(len(seq['tokens'])*seq['feature_dim']);router=max(features['router_weights']) if features['router_weights'] else 0.0
    violations=[]
    if mean_shift>policy.max_mean_shift:violations.append('mean_shift')
    if scale_ratio>policy.max_scale_ratio:violations.append('scale_ratio')
    if missing>policy.max_missing_rate:violations.append('missing_rate')
    if router>policy.max_router_concentration:violations.append('router_concentration')
    if len(seq['tokens'])<policy.min_support_tokens:violations.append('insufficient_support')
    supported=not violations;score=clamp(1.0-.15*mean_shift-.1*max(0,scale_ratio-1)-missing-.2*router,0,1)
    doc={'phase':'SAED_V4_14','candidate_id':candidate.candidate_id,'mean_shift':mean_shift,'scale_ratio':scale_ratio,'missing_rate':missing,'router_concentration':router,'support_tokens':len(seq['tokens']),'violations':violations,'supported':supported,'unsupported_action':'none' if supported else policy.unsupported_action,'robustness_score':score,'runtime_authority':False}
    doc['domain_shift_hash']=content_hash(doc);doc['domain_shift_id']=stable_id('fmdomain',doc);return doc
