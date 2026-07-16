from __future__ import annotations
import math

def clamp(x,lo=0.0,hi=1.0): return min(float(hi),max(float(lo),float(x)))
def mean(xs): return sum(xs)/len(xs) if xs else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((x-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def sigmoid(x):
    x=min(40.0,max(-40.0,float(x))); return 1.0/(1.0+math.exp(-x))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(map(float,xs)); p=clamp(q)*(len(ys)-1); lo=int(math.floor(p)); hi=int(math.ceil(p)); a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def correlation(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2:return 0.0
    mx,my=mean(xs),mean(ys); sx,sy=std(xs),std(ys)
    return sum((a-mx)*(b-my) for a,b in zip(xs,ys))/((len(xs)-1)*sx*sy) if sx>1e-12 and sy>1e-12 else 0.0
def fuzzy_not(x): return 1.0-clamp(x)
def fuzzy_and(xs,kind='product'):
    xs=[clamp(x) for x in xs]
    if not xs:return 1.0
    if kind=='minimum':return min(xs)
    if kind=='lukasiewicz':return max(0.0,sum(xs)-(len(xs)-1))
    p=1.0
    for x in xs:p*=x
    return p
def fuzzy_or(xs,kind='probabilistic_sum'):
    xs=[clamp(x) for x in xs]
    if not xs:return 0.0
    if kind=='maximum':return max(xs)
    if kind=='lukasiewicz':return min(1.0,sum(xs))
    p=1.0
    for x in xs:p*=1.0-x
    return 1.0-p
