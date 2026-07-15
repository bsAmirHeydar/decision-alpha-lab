from __future__ import annotations
import math
from .errors import NumericalError

def finite(x):
    x=float(x)
    if not math.isfinite(x): raise NumericalError('non-finite numeric value')
    return x

def dot(a,b):
    if len(a)!=len(b): raise NumericalError('dot width mismatch')
    return sum(finite(x)*finite(y) for x,y in zip(a,b))
def add(a,b):
    if len(a)!=len(b): raise NumericalError('add width mismatch')
    return tuple(finite(x)+finite(y) for x,y in zip(a,b))
def scale(a,s): return tuple(finite(x)*finite(s) for x in a)
def mean(rows):
    if not rows:return ()
    d=len(rows[0])
    if any(len(r)!=d for r in rows): raise NumericalError('row width mismatch')
    return tuple(sum(float(r[j]) for r in rows)/len(rows) for j in range(d))
def l2(a): return math.sqrt(max(0.0,dot(a,a)))
def cosine(a,b):
    d=l2(a)*l2(b)
    return 0.0 if d==0 else dot(a,b)/d
def tanh_vec(a): return tuple(math.tanh(max(-30.0,min(30.0,finite(x)))) for x in a)
def softmax(xs):
    if not xs:return ()
    m=max(xs);es=[math.exp(max(-50,min(50,x-m))) for x in xs];s=sum(es)
    return tuple(x/s for x in es)
def matvec(m,v): return tuple(dot(row,v) for row in m)
def max_abs_diff(a,b):
    if len(a)!=len(b): raise NumericalError('diff width mismatch')
    return max((abs(float(x)-float(y)) for x,y in zip(a,b)),default=0.0)
def solve_linear(a,b):
    n=len(a)
    if n==0 or len(b)!=n or any(len(r)!=n for r in a): raise NumericalError('bad linear system')
    m=[list(map(float,a[i]))+[float(b[i])] for i in range(n)]
    for c in range(n):
        p=max(range(c,n),key=lambda r:abs(m[r][c]))
        if abs(m[p][c])<1e-12: raise NumericalError('singular system')
        m[c],m[p]=m[p],m[c];q=m[c][c];m[c]=[x/q for x in m[c]]
        for r in range(n):
            if r==c:continue
            q=m[r][c]
            if q:m[r]=[x-q*y for x,y in zip(m[r],m[c])]
    return tuple(m[i][-1] for i in range(n))
def ridge_fit(xs,ys,alpha=1e-3):
    if not xs or len(xs)!=len(ys): raise NumericalError('empty ridge data')
    p=len(xs[0])+1;q=len(ys[0]);ata=[[0.0]*p for _ in range(p)];aty=[[0.0]*q for _ in range(p)]
    for x,y in zip(xs,ys):
        if len(x)+1!=p or len(y)!=q: raise NumericalError('ridge width mismatch')
        z=(1.0,*map(float,x))
        for i in range(p):
            for j in range(p): ata[i][j]+=z[i]*z[j]
            for k in range(q): aty[i][k]+=z[i]*float(y[k])
    for i in range(1,p):ata[i][i]+=alpha
    cols=[solve_linear(ata,[aty[i][k] for i in range(p)]) for k in range(q)]
    return tuple(tuple(cols[k][i] for k in range(q)) for i in range(p))
def ridge_predict(w,x):
    z=(1.0,*map(float,x));return tuple(sum(z[i]*w[i][k] for i in range(len(z))) for k in range(len(w[0])))
