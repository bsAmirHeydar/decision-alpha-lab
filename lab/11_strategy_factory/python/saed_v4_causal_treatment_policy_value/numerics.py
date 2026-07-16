from __future__ import annotations
import math

def clamp(x,lo,hi): return min(hi,max(lo,float(x)))
def mean(xs): return sum(xs)/len(xs) if xs else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((x-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(map(float,xs));p=clamp(q,0,1)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def covariance(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2:return 0.0
    mx,my=mean(xs),mean(ys);return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(len(xs)-1)
def correlation(xs,ys):
    sx,sy=std(xs),std(ys);return covariance(xs,ys)/(sx*sy) if sx>1e-15 and sy>1e-15 else 0.0
def sigmoid(x):
    x=clamp(x,-40,40);return 1/(1+math.exp(-x))
def softmax(xs):
    if not xs:return []
    m=max(xs);e=[math.exp(clamp(x-m,-40,40)) for x in xs];s=sum(e);return [v/s for v in e]
def transpose(x): return [list(v) for v in zip(*x)] if x else []
def solve(a,b,ridge=1e-8):
    n=len(b);m=[list(map(float,row))+[float(b[i])] for i,row in enumerate(a)]
    for i in range(n):m[i][i]+=ridge
    for c in range(n):
        pivot=max(range(c,n),key=lambda r:abs(m[r][c]))
        if abs(m[pivot][c])<1e-14:continue
        m[c],m[pivot]=m[pivot],m[c];d=m[c][c];m[c]=[v/d for v in m[c]]
        for r in range(n):
            if r==c:continue
            f=m[r][c]
            if f:m[r]=[x-f*y for x,y in zip(m[r],m[c])]
    return [m[i][-1] if abs(m[i][i])>1e-14 else 0.0 for i in range(n)]
def ridge_fit(x,y,ridge=1e-5):
    if not y:return [0.0]
    if not x:return [mean(y)]
    design=[[1.0]+list(map(float,row)) for row in x];cols=transpose(design);p=len(cols)
    gram=[[sum(cols[i][k]*cols[j][k] for k in range(len(y))) for j in range(p)] for i in range(p)]
    rhs=[sum(cols[i][k]*float(y[k]) for k in range(len(y))) for i in range(p)]
    return solve(gram,rhs,ridge)
def predict(beta,x): return beta[0]+sum(b*v for b,v in zip(beta[1:],x))
def rmse(y,p): return math.sqrt(mean([(a-b)**2 for a,b in zip(y,p)])) if y else 0.0
def mae(y,p): return mean([abs(a-b) for a,b in zip(y,p)]) if y else 0.0
def effective_sample_size(weights):
    s=sum(weights);d=sum(w*w for w in weights);return s*s/d if d>1e-15 else 0.0
def normal_lcb(value,se,z=1.96): return float(value)-float(z)*max(0.0,float(se))
def cvar_lower(xs,alpha=0.1):
    if not xs:return 0.0
    k=max(1,int(math.ceil(len(xs)*clamp(alpha,0.001,1.0))));return mean(sorted(xs)[:k])
