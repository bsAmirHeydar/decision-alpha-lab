from __future__ import annotations
import math

def _validate(y, p):
    if len(y)!=len(p) or not y: raise ValueError("metric vectors must be non-empty and aligned")

def binary_log_loss(y, p, epsilon: float=1e-12) -> float:
    _validate(y,p);total=0.0
    for target,probability in zip(y,p):
        q=min(1-epsilon,max(epsilon,probability))
        total += -(target*math.log(q)+(1-target)*math.log(1-q))
    return total/len(y)

def brier_score(y,p)->float:
    _validate(y,p);return sum((a-b)**2 for a,b in zip(y,p))/len(y)

def accuracy(y,p,threshold:float=0.5)->float:
    _validate(y,p);return sum((1 if q>=threshold else 0)==int(t) for t,q in zip(y,p))/len(y)

def precision_recall(y,p,threshold:float=0.5)->tuple[float,float]:
    _validate(y,p);pred=[1 if q>=threshold else 0 for q in p]
    tp=sum(a==1 and b==1 for a,b in zip(y,pred));fp=sum(a==0 and b==1 for a,b in zip(y,pred));fn=sum(a==1 and b==0 for a,b in zip(y,pred))
    return (tp/(tp+fp) if tp+fp else 0.0,tp/(tp+fn) if tp+fn else 0.0)

def roc_auc(y,p)->float:
    _validate(y,p);positive=sum(int(v==1) for v in y);negative=len(y)-positive
    if positive==0 or negative==0:return 0.5
    order=sorted(range(len(p)),key=lambda i:(p[i],i));ranks=[0.0]*len(p);i=0
    while i<len(order):
        j=i+1
        while j<len(order) and p[order[j]]==p[order[i]]:j+=1
        rank=(i+1+j)/2.0
        for k in range(i,j):ranks[order[k]]=rank
        i=j
    sum_pos=sum(ranks[i] for i,v in enumerate(y) if v==1)
    return (sum_pos-positive*(positive+1)/2)/(positive*negative)

def expected_calibration_error(y,p,bins:int=10)->float:
    _validate(y,p)
    if bins<2:raise ValueError("bins must be at least two")
    total=0.0
    for index in range(bins):
        low=index/bins;high=(index+1)/bins
        members=[i for i,q in enumerate(p) if (low<=q<high or (index==bins-1 and q==1.0))]
        if members:
            confidence=sum(p[i] for i in members)/len(members);frequency=sum(y[i] for i in members)/len(members)
            total += len(members)/len(y)*abs(confidence-frequency)
    return total

def regression_metrics(y,p)->dict[str,float]:
    _validate(y,p);errors=[a-b for a,b in zip(y,p)]
    mae=sum(abs(e) for e in errors)/len(errors);rmse=math.sqrt(sum(e*e for e in errors)/len(errors))
    mean=sum(y)/len(y);den=sum((a-mean)**2 for a in y);r2=1-sum(e*e for e in errors)/den if den>0 else 0.0
    return {"mae":mae,"rmse":rmse,"r2":r2}

def score_binary(y,p)->dict[str,float]:
    precision,recall=precision_recall(y,p)
    return {"log_loss":binary_log_loss(y,p),"brier":brier_score(y,p),"accuracy":accuracy(y,p),
            "auc":roc_auc(y,p),"precision":precision,"recall":recall,
            "ece":expected_calibration_error(y,p)}
