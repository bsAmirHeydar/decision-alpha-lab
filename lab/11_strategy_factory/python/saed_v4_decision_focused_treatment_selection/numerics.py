from __future__ import annotations
import math

def clamp(x,lo=0.0,hi=1.0): return min(float(hi),max(float(lo),float(x)))
def mean(xs): return sum(map(float,xs))/len(xs) if xs else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((float(x)-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(map(float,xs));p=clamp(q)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def median(xs): return quantile(xs,0.5)
def softmax(xs,temperature=1.0):
    if not xs:return []
    t=max(1e-9,float(temperature));m=max(xs);ws=[math.exp((x-m)/t) for x in xs];s=sum(ws)
    return [w/s for w in ws]
def entropy(ps): return -sum(p*math.log(max(p,1e-15)) for p in ps)
def lcb(mu,sigma,z): return float(mu)-abs(float(z))*max(0.0,float(sigma))
def ucb(mu,sigma,z): return float(mu)+abs(float(z))*max(0.0,float(sigma))
def cvar_lower(xs,alpha=0.1):
    if not xs:return 0.0
    ys=sorted(map(float,xs));k=max(1,int(math.ceil(clamp(alpha,1e-6,1.0)*len(ys))))
    return mean(ys[:k])
def max_drawdown(xs):
    peak=0.0;curve=0.0;worst=0.0
    for x in xs:
        curve+=float(x);peak=max(peak,curve);worst=max(worst,peak-curve)
    return worst
def rankdata_desc(values):
    order=sorted(range(len(values)),key=lambda i:(-values[i],i));r=[0]*len(values)
    for k,i in enumerate(order,1):r[i]=k
    return r
