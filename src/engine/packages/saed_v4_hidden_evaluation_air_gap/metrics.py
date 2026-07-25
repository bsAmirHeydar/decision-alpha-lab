from __future__ import annotations
import math

def sigmoid(x:float)->float:
    if x>=0: z=math.exp(-x); return 1.0/(1.0+z)
    z=math.exp(x); return z/(1.0+z)
def predict(model,features):
    z=float(model["intercept"])
    for name,weight in zip(model["feature_order"],model["weights"]):
        if name not in features: raise ValueError(f"missing feature {name}")
        z+=float(weight)*float(features[name])
    p=sigmoid(z); return p,1 if p>=0.5 else 0

def auc(labels,scores):
    pos=[s for y,s in zip(labels,scores) if y==1]; neg=[s for y,s in zip(labels,scores) if y==0]
    if not pos or not neg: return 0.5
    wins=0.0
    for p in pos:
        for n in neg: wins+=1.0 if p>n else 0.5 if p==n else 0.0
    return wins/(len(pos)*len(neg))
def calculate(labels,scores,preds):
    n=len(labels); eps=1e-15
    tp=sum(y==1 and p==1 for y,p in zip(labels,preds)); tn=sum(y==0 and p==0 for y,p in zip(labels,preds)); fp=sum(y==0 and p==1 for y,p in zip(labels,preds)); fn=sum(y==1 and p==0 for y,p in zip(labels,preds))
    tpr=tp/(tp+fn) if tp+fn else 0.0; tnr=tn/(tn+fp) if tn+fp else 0.0
    return {"accuracy":(tp+tn)/n,"balanced_accuracy":0.5*(tpr+tnr),"brier_score":sum((s-y)**2 for y,s in zip(labels,scores))/n,"log_loss":-sum(y*math.log(max(eps,min(1-eps,s)))+(1-y)*math.log(max(eps,min(1-eps,1-s))) for y,s in zip(labels,scores))/n,"roc_auc":auc(labels,scores)}
