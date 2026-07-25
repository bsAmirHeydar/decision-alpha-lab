from math import log,sqrt
def binary_metrics(y,p,w,t=.5):
 total=sum(w);eps=1e-15
 return {'brier':sum(a*(b-c)**2 for c,b,a in zip(y,p,w))/total,'log_loss':-sum(a*(c*log(max(eps,min(1-eps,b)))+(1-c)*log(max(eps,min(1-eps,1-b)))) for c,b,a in zip(y,p,w))/total,'accuracy':sum(a*((b>=t)==(c>=.5)) for c,b,a in zip(y,p,w))/total}
def regression_metrics(y,p,w):
 total=sum(w);mse=sum(a*(b-c)**2 for c,b,a in zip(y,p,w))/total
 return {'mse':mse,'rmse':sqrt(mse),'mae':sum(a*abs(b-c) for c,b,a in zip(y,p,w))/total}
def ranking_metrics(y,p,g,w):
 by={}
 for i,q in enumerate(g):by.setdefault(q,[]).append(i)
 ok=tot=0.
 for ids in by.values():
  for a in range(len(ids)):
   for b in range(a+1,len(ids)):
    i,j=ids[a],ids[b]
    if y[i]==y[j]:continue
    ww=(w[i]+w[j])/2;tot+=ww;ok+=ww*(((p[i]-p[j])*(y[i]-y[j]))>0)
 return {'pairwise_accuracy':ok/tot if tot else .5,'pair_count':tot}
