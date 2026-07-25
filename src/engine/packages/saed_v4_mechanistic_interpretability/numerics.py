from __future__ import annotations
import math
from typing import Iterable

def dot(left: Iterable[float], right: Iterable[float]) -> float:
    a, b = list(left), list(right)
    if len(a) != len(b):
        raise ValueError("dimension mismatch")
    return sum(x*y for x, y in zip(a,b))

def mean(values: Iterable[float]) -> float:
    xs = list(values)
    return sum(xs)/len(xs) if xs else 0.0

def sigmoid(value: float) -> float:
    if value >= 0:
        z = math.exp(-value)
        return 1.0/(1.0+z)
    z = math.exp(value)
    return z/(1.0+z)

def cosine(left: Iterable[float], right: Iterable[float]) -> float:
    a, b = list(left), list(right)
    if len(a) != len(b) or not a:
        return 0.0
    denom = math.sqrt(dot(a,a))*math.sqrt(dot(b,b))
    return dot(a,b)/denom if denom else 0.0

def pearson(left: Iterable[float], right: Iterable[float]) -> float:
    a,b=list(left),list(right)
    if len(a)!=len(b) or len(a)<2:
        return 0.0
    ma,mb=mean(a),mean(b)
    da=[x-ma for x in a]; db=[x-mb for x in b]
    denom=math.sqrt(dot(da,da)*dot(db,db))
    return dot(da,db)/denom if denom else 0.0

def rank(values: Iterable[float]) -> list[int]:
    xs=list(values)
    order=sorted(range(len(xs)), key=lambda i:(xs[i],i))
    out=[0]*len(xs)
    for r,i in enumerate(order): out[i]=r
    return out

def rank_correlation(left: Iterable[float], right: Iterable[float]) -> float:
    return pearson(rank(left),rank(right))

def quantile(values: Iterable[float], q: float) -> float:
    xs=sorted(values)
    if not xs: return 0.0
    pos=(len(xs)-1)*q; lo=int(math.floor(pos)); hi=int(math.ceil(pos))
    if lo==hi: return xs[lo]
    return xs[lo]*(hi-pos)+xs[hi]*(pos-lo)
