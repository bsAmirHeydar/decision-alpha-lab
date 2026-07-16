from __future__ import annotations
from datetime import datetime,timezone
from .canonical import hash_signed,content_hash,stable_id

def _dt(s): return datetime.fromisoformat(s.replace('Z','+00:00'))
def _scalar(v,key):
    if isinstance(v,bool):return 1.0 if v else 0.0
    if isinstance(v,(int,float)):return float(v)
    if isinstance(v,str):return hash_signed(key+'|'+v)
    if isinstance(v,list):return sum(_scalar(x,key+f'|{i}') for i,x in enumerate(v))/max(1,len(v))
    if v is None:return 0.0
    return hash_signed(key+'|'+str(v))

def encode_domain_view(view,config,cutoff):
    future=_dt(view['known_as_of'])>_dt(cutoff)
    features=[];quality=[];missing=[]
    for f in sorted(view.get('features',[]),key=lambda x:x['feature_id']):
        is_missing=bool(f.get('missing')) or future
        missing.append(is_missing);quality.append(float(f.get('quality',0.0)) if not is_missing else 0.0)
        if is_missing:continue
        features.append((f['feature_id'],_scalar(f.get('normalized_value'),view['view_name']+'|'+f['feature_id']),float(f.get('quality',0.0))))
    vec=[]
    for d in range(config.common_dim):
        num=sum(val*q*hash_signed(f"{view['view_name']}|{fid}|{d}") for fid,val,q in features);den=sum(q for _,_,q in features) or 1.0
        vec.append(math_tanh(num/den))
    support=float(view.get('support',{}).get('score',0.0));q=(sum(quality)/len(quality) if quality else 0.0)*support
    age=max(0,int((_dt(cutoff)-_dt(view['known_as_of'])).total_seconds()))
    available=not future and view.get('status') in {'complete','degraded'} and q>=config.min_view_quality and age<=config.max_view_age_seconds and not all(missing)
    doc={'phase':'SAED_V4_15','source_plane':'domain','view_name':view['view_name'],'view_kind':view['kind'],'source_view_id':view['view_id'],'source_view_hash':view['view_hash'],'known_as_of':view['known_as_of'],'cutoff':cutoff,'age_seconds':age,'quality':q,'missing_feature_count':sum(missing),'feature_count':len(missing),'available':available,'future_filtered':future,'embedding':vec,'embedding_dim':config.common_dim,'production_eligible':False}
    doc['envelope_hash']=content_hash(doc);doc['envelope_id']=stable_id('v415view',doc);return doc

def math_tanh(x):
    import math
    return math.tanh(float(x))

def encode_foundation_feature(feature,config,domain_by_candidate,calibration_by_candidate):
    raw=list(map(float,feature['embedding']));vec=[]
    for d in range(config.common_dim):
        if d<len(raw):v=raw[d]
        else:v=sum(raw[i]*hash_signed(f"{feature['candidate_id']}|{i}|{d}") for i in range(len(raw)))/max(1,len(raw))
        vec.append(math_tanh(v))
    dom=domain_by_candidate.get(feature['candidate_id'],{});cal=calibration_by_candidate.get(feature['candidate_id'],{})
    supported=bool(dom.get('supported',True)) and bool(cal.get('quantile_monotonic',True));q=1.0/(1.0+float(feature.get('uncertainty_scale',1.0)))
    if not supported:q*=0.25
    doc={'phase':'SAED_V4_15','source_plane':'foundation','view_name':'foundation_'+feature['family'],'view_kind':'foundation_adapter','source_candidate_id':feature['candidate_id'],'source_feature_id':feature['feature_id'],'source_feature_hash':feature['feature_hash'],'known_as_of':feature['known_as_of'],'age_seconds':0,'quality':q,'uncertainty':float(feature['uncertainty_scale']),'available':supported and not feature['future_suffix_accessed'],'embedding':vec,'embedding_dim':config.common_dim,'external_model_invoked':False,'production_eligible':False}
    doc['envelope_hash']=content_hash(doc);doc['envelope_id']=stable_id('v415foundation',doc);return doc
