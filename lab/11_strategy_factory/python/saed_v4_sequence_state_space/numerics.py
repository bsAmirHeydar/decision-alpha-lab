from __future__ import annotations
import math
from .errors import NumericalError

def finite(x:float)->float:
    x=float(x)
    if not math.isfinite(x): raise NumericalError('non-finite numeric value')
    return x

def sigmoid(x:float)->float:
    x=max(-40.0,min(40.0,finite(x))); return 1.0/(1.0+math.exp(-x))
def tanh(x:float)->float: return math.tanh(max(-40.0,min(40.0,finite(x))))
def softplus(x:float)->float:
    x=finite(x)
    if x>30:return x
    if x<-30:return math.exp(x)
    return math.log1p(math.exp(x))
def dot(a,b):
    if len(a)!=len(b): raise NumericalError('dot width mismatch')
    return sum(finite(x)*finite(y) for x,y in zip(a,b))
def add(a,b):
    if len(a)!=len(b): raise NumericalError('add width mismatch')
    return tuple(finite(x)+finite(y) for x,y in zip(a,b))
def scale(a,s): return tuple(finite(x)*finite(s) for x in a)
def mean_vec(rows):
    if not rows:return ()
    n=len(rows);d=len(rows[0])
    if any(len(r)!=d for r in rows):raise NumericalError('row width mismatch')
    return tuple(sum(float(r[j]) for r in rows)/n for j in range(d))
def l2(a): return math.sqrt(max(0.0,dot(a,a)))
def cosine(a,b):
    den=l2(a)*l2(b)
    return 0.0 if den==0 else dot(a,b)/den
def max_abs_diff(a,b):
    if len(a)!=len(b): raise NumericalError('diff width mismatch')
    return max((abs(float(x)-float(y)) for x,y in zip(a,b)),default=0.0)
def matvec(m,v): return tuple(dot(row,v) for row in m)
def outer(a,b): return [[float(x)*float(y) for y in b] for x in a]

def solve_linear(a,b):
    n=len(a)
    if n==0 or any(len(row)!=n for row in a) or len(b)!=n: raise NumericalError('invalid linear system')
    m=[list(map(float,row))+[float(b[i])] for i,row in enumerate(a)]
    for col in range(n):
        pivot=max(range(col,n),key=lambda r:abs(m[r][col]))
        if abs(m[pivot][col])<1e-12: raise NumericalError('singular linear system')
        m[col],m[pivot]=m[pivot],m[col]
        p=m[col][col];m[col]=[x/p for x in m[col]]
        for r in range(n):
            if r==col:continue
            f=m[r][col]
            if f:m[r]=[x-f*y for x,y in zip(m[r],m[col])]
    return tuple(m[i][-1] for i in range(n))

def ridge_fit(xs,ys,alpha=1e-3):
    if not xs or len(xs)!=len(ys): raise NumericalError('empty or mismatched ridge data')
    p=len(xs[0])+1;q=len(ys[0])
    if any(len(x)+1!=p for x in xs) or any(len(y)!=q for y in ys): raise NumericalError('ridge row width mismatch')
    ata=[[0.0]*p for _ in range(p)];aty=[[0.0]*q for _ in range(p)]
    for x,y in zip(xs,ys):
        z=(1.0,*map(float,x))
        for i in range(p):
            for j in range(p):ata[i][j]+=z[i]*z[j]
            for k in range(q):aty[i][k]+=z[i]*float(y[k])
    for i in range(1,p):ata[i][i]+=alpha
    cols=[solve_linear(ata,[aty[i][k] for i in range(p)]) for k in range(q)]
    return tuple(tuple(cols[k][i] for k in range(q)) for i in range(p))
def ridge_predict(weights,x):
    z=(1.0,*map(float,x));q=len(weights[0])
    return tuple(sum(z[i]*weights[i][k] for i in range(len(z))) for k in range(q))
