from __future__ import annotations
import math,random

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
def normalize(xs):
    ys=[max(0.0,float(x)) for x in xs];s=sum(ys)
    return [x/s for x in ys] if s>0 else ([1.0/len(ys)]*len(ys) if ys else [])
def softmax(values,temperature=1.0):
    if not values:return []
    t=max(float(temperature),1e-9);m=max(values);ex=[math.exp((float(x)-m)/t) for x in values];return normalize(ex)
def logsumexp(values):
    if not values:return float('-inf')
    m=max(values);return m+math.log(sum(math.exp(float(x)-m) for x in values))
def argmax_key(mapping): return sorted(mapping,key=lambda k:(-float(mapping[k]),str(k)))[0]
def l1_distribution(a,b,keys): return sum(abs(float(a.get(k,0.0))-float(b.get(k,0.0))) for k in keys)
def kl_divergence(p,q,keys,eps=1e-12):
    return sum(max(eps,float(p.get(k,0.0)))*math.log(max(eps,float(p.get(k,0.0)))/max(eps,float(q.get(k,0.0)))) for k in keys)
def effective_sample_size(weights):
    s=sum(weights);d=sum(float(w)**2 for w in weights)
    return (s*s/d) if d>0 else 0.0
def weighted_mean(values,weights):
    s=sum(weights);return sum(float(v)*float(w) for v,w in zip(values,weights))/s if s>0 else 0.0
def bootstrap_ci(values,seed=423,draws=300,alpha=0.05):
    values=list(map(float,values))
    if not values:return {'mean':0.0,'lower':0.0,'upper':0.0,'draws':0}
    rng=random.Random(int(seed));means=[];n=len(values)
    for _ in range(int(draws)): means.append(mean([values[rng.randrange(n)] for _ in range(n)]))
    return {'mean':mean(values),'lower':quantile(means,alpha/2),'upper':quantile(means,1-alpha/2),'draws':int(draws)}
def expectile(values,weights,tau=0.7,iterations=40):
    if not values:return 0.0
    v=weighted_mean(values,weights)
    for _ in range(iterations):
        asym=[float(w)*(tau if float(x)>=v else 1-tau) for x,w in zip(values,weights)]
        v=weighted_mean(values,asym)
    return v
