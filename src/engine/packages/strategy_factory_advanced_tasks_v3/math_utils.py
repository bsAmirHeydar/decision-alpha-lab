from math import exp,log,sqrt

def dot(a,b):return sum(float(x)*float(y) for x,y in zip(a,b))
def sigmoid(x):
 if x>=0:
  z=exp(-x);return 1/(1+z)
 z=exp(x);return z/(1+z)
def weighted_mean(values,weights):
 s=sum(weights);return sum(v*w for v,w in zip(values,weights))/s if s else 0.0
def weighted_quantile(values,weights,q):
 if not values:return 0.0
 pairs=sorted((float(v),max(0.,float(w))) for v,w in zip(values,weights));total=sum(w for _,w in pairs)
 if total<=0:return pairs[min(len(pairs)-1,max(0,int(q*(len(pairs)-1))))][0]
 target=min(1.,max(0.,q))*total;c=0.
 for v,w in pairs:
  c+=w
  if c>=target:return v
 return pairs[-1][0]
def mean(v):return sum(v)/len(v) if v else 0.
def stdev(v):
 if len(v)<2:return 0.
 m=mean(v);return sqrt(sum((x-m)**2 for x in v)/(len(v)-1))
def normal_lcb(mean_value,se,z=1.96):return mean_value-z*se

def fit_ridge(x,y,weights=None,alpha=1e-3,steps=400,lr=0.03):
 if not x:return (),0.
 n=len(x);p=len(x[0]);w=[0.]*p;b=0.;sw=weights or [1.]*n;den=sum(sw) or 1.
 scale=[max(1.,sqrt(sum(sw[i]*x[i][j]*x[i][j] for i in range(n))/den)) for j in range(p)]
 for _ in range(max(1,steps)):
  gw=[0.]*p;gb=0.
  for row,t,ww in zip(x,y,sw):
   pred=b+sum(w[j]*(row[j]/scale[j]) for j in range(p));e=pred-t;gb+=ww*e
   for j in range(p):gw[j]+=ww*e*(row[j]/scale[j])
  b-=lr*2*gb/den
  for j in range(p):w[j]-=lr*2*(gw[j]/den+alpha*w[j])
 return tuple(w[j]/scale[j] for j in range(p)),b
