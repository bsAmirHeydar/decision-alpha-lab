from __future__ import annotations
import math,statistics

def mean(xs): return sum(map(float,xs))/len(xs) if xs else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((float(x)-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def clamp(x,lo=0.0,hi=1.0): return min(float(hi),max(float(lo),float(x)))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(map(float,xs));p=clamp(q)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def autocorr(xs,lag=1):
    if len(xs)<=lag:return 0.0
    a=list(map(float,xs[:-lag]));b=list(map(float,xs[lag:]));ma=mean(a);mb=mean(b)
    den=math.sqrt(sum((x-ma)**2 for x in a)*sum((x-mb)**2 for x in b))
    return sum((x-ma)*(y-mb) for x,y in zip(a,b))/den if den else 0.0
def l1(a,b): return sum(abs(float(x)-float(y)) for x,y in zip(a,b))
def normalize(xs):
    ys=[max(0.0,float(x)) for x in xs];s=sum(ys)
    return [x/s for x in ys] if s else ([1.0/len(ys)]*len(ys) if ys else [])
def rmse(a,b): return math.sqrt(mean([(float(x)-float(y))**2 for x,y in zip(a,b)])) if a else 0.0
def max_drawdown(returns):
    curve=peak=worst=0.0
    for r in returns:
        curve+=float(r);peak=max(peak,curve);worst=max(worst,peak-curve)
    return worst
def finite(x): return math.isfinite(float(x))
