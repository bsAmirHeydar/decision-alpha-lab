from __future__ import annotations
import math

def mean(vs):
    if not vs: return tuple()
    n=len(vs);d=len(vs[0]);return tuple(sum(float(v[i]) for v in vs)/n for i in range(d))
def std(xs):
    if not xs:return 0.0
    m=sum(xs)/len(xs);return math.sqrt(sum((x-m)**2 for x in xs)/len(xs))
def dot(a,b): return sum(float(x)*float(y) for x,y in zip(a,b))
def l2(a,b): return math.sqrt(sum((float(x)-float(y))**2 for x,y in zip(a,b)))
def tanh_vec(v): return tuple(math.tanh(float(x)) for x in v)
def softmax(xs):
    if not xs:return tuple()
    m=max(xs);e=[math.exp(x-m) for x in xs];s=sum(e);return tuple(x/s for x in e)
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(float(x) for x in xs);p=(len(ys)-1)*q;i=int(p);j=min(i+1,len(ys)-1);return ys[i]+(p-i)*(ys[j]-ys[i])
def clamp(x,a,b): return max(a,min(b,x))
