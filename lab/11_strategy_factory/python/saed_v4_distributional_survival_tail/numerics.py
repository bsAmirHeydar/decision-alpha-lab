from __future__ import annotations
import math

def clamp(x,lo,hi): return min(hi,max(lo,float(x)))
def mean(xs): return sum(xs)/len(xs) if xs else 0.0
def weighted_mean(xs,ws):
    s=sum(ws);return sum(x*w for x,w in zip(xs,ws))/s if s else 0.0
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(float(x) for x in xs);p=clamp(q,0,1)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def monotone(xs):
    out=[];m=-float('inf')
    for x in xs:m=max(m,float(x));out.append(m)
    return out
def sigmoid(x):
    x=clamp(x,-40,40);return 1/(1+math.exp(-x))
def pinball(y,qhat,q):
    e=float(y)-float(qhat);return max(q*e,(q-1)*e)
def safe_div(a,b,default=0.0): return a/b if b else default
def l1(a,b): return sum(abs(x-y) for x,y in zip(a,b))/max(1,len(a))
def isotonic_probabilities(xs):
    out=[];m=0.0
    for x in xs:m=max(m,clamp(x,0,1));out.append(m)
    if out and out[-1]>1:out=[x/out[-1] for x in out]
    return out
