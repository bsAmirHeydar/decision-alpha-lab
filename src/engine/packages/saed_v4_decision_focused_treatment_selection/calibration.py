from __future__ import annotations
import math
from .numerics import softmax,clamp
from .errors import CalibrationError

def calibrate_scores(ranked,method='identity',temperature=1.0):
    xs=[float(r['objective_score']) for r in ranked]
    if method=='identity':ps=softmax(xs,1.0)
    elif method=='temperature':ps=softmax(xs,max(1e-6,float(temperature)))
    elif method=='platt_reference':ps=softmax([1.25*x-0.05 for x in xs],1.0)
    elif method=='isotonic_reference':
        raw=softmax(xs,1.0);ps=[];floor=0.0
        for p in raw[::-1]:floor=max(floor,p);ps.append(floor)
        ps=list(reversed(ps));s=sum(ps);ps=[p/s for p in ps]
    else:raise CalibrationError('unknown calibration method')
    out=[]
    for r,p in zip(ranked,ps):x=dict(r);x['selection_probability']=clamp(p);out.append(x)
    return out

def expected_calibration_error(probabilities,correct,bins=5):
    n=len(probabilities)
    if n==0:return 0.0
    e=0.0
    for b in range(bins):
        lo=b/bins;hi=(b+1)/bins;idx=[i for i,p in enumerate(probabilities) if lo<=p<hi or (b==bins-1 and p==1)]
        if idx:
            conf=sum(probabilities[i] for i in idx)/len(idx);acc=sum(bool(correct[i]) for i in idx)/len(idx);e+=len(idx)/n*abs(conf-acc)
    return e
