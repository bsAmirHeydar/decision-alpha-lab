from __future__ import annotations
import math

def clamp(x,lo,hi): return min(hi,max(lo,float(x)))
def mean(xs): return sum(xs)/len(xs) if xs else 0.0
def variance(xs):
    if len(xs)<2:return 0.0
    m=mean(xs);return sum((x-m)**2 for x in xs)/(len(xs)-1)
def std(xs): return math.sqrt(max(0.0,variance(xs)))
def covariance(xs,ys):
    if len(xs)!=len(ys) or len(xs)<2:return 0.0
    mx,my=mean(xs),mean(ys);return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/(len(xs)-1)
def correlation(xs,ys):
    sx,sy=std(xs),std(ys);return covariance(xs,ys)/(sx*sy) if sx>1e-15 and sy>1e-15 else 0.0
def sigmoid(x):
    x=clamp(x,-40,40);return 1/(1+math.exp(-x))
def rmse(xs): return math.sqrt(mean([x*x for x in xs])) if xs else 0.0
def mae(xs): return mean([abs(x) for x in xs])
def l1(a,b): return mean([abs(x-y) for x,y in zip(a,b)]) if a and b else 0.0
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
def ridge_fit(x,y,ridge=1e-6):
    if not x:return [mean(y)]
    design=[[1.0]+list(map(float,row)) for row in x];cols=transpose(design);p=len(cols)
    gram=[[sum(cols[i][k]*cols[j][k] for k in range(len(y))) for j in range(p)] for i in range(p)]
    rhs=[sum(cols[i][k]*float(y[k]) for k in range(len(y))) for i in range(p)]
    return solve(gram,rhs,ridge)
def predict(beta,x): return beta[0]+sum(b*v for b,v in zip(beta[1:],x))
def residualize(y,x):
    if not x:return [v-mean(y) for v in y]
    beta=ridge_fit(x,y);return [v-predict(beta,row) for v,row in zip(y,x)]
def partial_correlation(x,y,z): return correlation(residualize(x,z),residualize(y,z))
def quantile(xs,q):
    if not xs:return 0.0
    ys=sorted(xs);p=clamp(q,0,1)*(len(ys)-1);lo=int(math.floor(p));hi=int(math.ceil(p));a=p-lo
    return ys[lo]*(1-a)+ys[hi]*a
def topological_sort(nodes,edges):
    incoming={n:0 for n in nodes};adj={n:[] for n in nodes}
    for a,b in edges:
        if a not in incoming or b not in incoming:continue
        incoming[b]+=1;adj[a].append(b)
    q=sorted([n for n,d in incoming.items() if d==0]);out=[]
    while q:
        n=q.pop(0);out.append(n)
        for v in sorted(adj[n]):
            incoming[v]-=1
            if incoming[v]==0:q.append(v);q.sort()
    return out if len(out)==len(nodes) else []
