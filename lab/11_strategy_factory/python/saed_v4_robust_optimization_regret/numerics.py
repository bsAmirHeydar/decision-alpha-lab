from __future__ import annotations
import math

def clamp(x,lo=0.0,hi=1.0): return min(float(hi),max(float(lo),float(x)))
def mean(xs): return sum(map(float,xs))/len(xs) if xs else 0.0
def weighted_mean(xs,ws):
    s=sum(map(float,ws));return sum(float(x)*float(w) for x,w in zip(xs,ws))/s if s else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((float(x)-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(map(float,xs));p=clamp(q)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def cvar_lower(xs,alpha=0.2):
    if not xs:return 0.0
    ys=sorted(map(float,xs));k=max(1,int(math.ceil(clamp(alpha,1e-9,1.0)*len(ys))))
    return mean(ys[:k])
def normalize(ws,floor=0.0):
    ys=[max(float(floor),float(x)) for x in ws];s=sum(ys)
    if s<=0:return [1.0/len(ys)]*len(ys) if ys else []
    return [x/s for x in ys]
def l1(a,b): return sum(abs(float(x)-float(y)) for x,y in zip(a,b))
def entropy(ps): return -sum(float(p)*math.log(max(float(p),1e-15)) for p in ps)
def max_drawdown(xs):
    curve=peak=worst=0.0
    for x in xs:
        curve+=float(x);peak=max(peak,curve);worst=max(worst,peak-curve)
    return worst
def almost_equal(a,b,tol=1e-12): return abs(float(a)-float(b))<=float(tol)
