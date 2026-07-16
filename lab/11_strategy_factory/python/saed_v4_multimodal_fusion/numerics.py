import math

def mean_vec(vs):
    if not vs:return tuple()
    return tuple(sum(float(v[i]) for v in vs)/len(vs) for i in range(len(vs[0])))
def weighted_mean(vs,ws):
    s=sum(ws)
    if s<=0:return tuple(0.0 for _ in vs[0])
    return tuple(sum(float(v[i])*w for v,w in zip(vs,ws))/s for i in range(len(vs[0])))
def l2(a,b):return math.sqrt(sum((float(x)-float(y))**2 for x,y in zip(a,b)))
def dot(a,b):return sum(float(x)*float(y) for x,y in zip(a,b))
def norm(a):return math.sqrt(max(dot(a,a),1e-18))
def cosine(a,b):return dot(a,b)/(norm(a)*norm(b))
def softmax(xs):
    m=max(xs);e=[math.exp(x-m) for x in xs];s=sum(e);return tuple(x/s for x in e)
def std(xs):
    if not xs:return 0.0
    m=sum(xs)/len(xs);return math.sqrt(sum((x-m)**2 for x in xs)/len(xs))
def clamp(x,a,b):return max(a,min(b,x))
