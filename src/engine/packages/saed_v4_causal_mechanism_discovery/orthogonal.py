from __future__ import annotations
from .canonical import content_hash
from .numerics import ridge_fit,predict,mean,variance

def reference_score(dataset,treatment,outcome,controls):
    rows=[r for r in dataset['rows'] if r['split']=='calibration'];x=[[r['values'][c] for c in controls] for r in rows];t=[r['values'][treatment] for r in rows];y=[r['values'][outcome] for r in rows]
    bt=ridge_fit(x,t);by=ridge_fit(x,y);rt=[v-predict(bt,row) for v,row in zip(t,x)];ry=[v-predict(by,row) for v,row in zip(y,x)];den=sum(v*v for v in rt);score=sum(a*b for a,b in zip(rt,ry))/den if den else 0.0
    influence=[a*(b-score*a) for a,b in zip(rt,ry)];se=(variance(influence)/max(1,len(influence)))**0.5/(mean([a*a for a in rt]) or 1.0)
    out={'phase':'SAED_V4_17','treatment_proxy_id':treatment,'outcome_proxy_id':outcome,'controls':controls,'evaluation_rows':len(rows),'orthogonal_association_score':score,'standard_error_reference':se,'lower_reference_bound':score-1.96*se,'upper_reference_bound':score+1.96*se,'causal_effect_claim_allowed':False,'production_eligible':False};out['report_hash']=content_hash(out);return out
