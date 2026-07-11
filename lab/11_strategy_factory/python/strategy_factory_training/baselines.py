from __future__ import annotations
from dataclasses import dataclass
import math
from .enums import ModelFamily, TaskKind

def sigmoid(value: float) -> float:
    if value>=0:
        z=math.exp(-min(value,700.0));return 1.0/(1.0+z)
    z=math.exp(max(value,-700.0));return z/(1.0+z)

@dataclass(frozen=True, slots=True)
class FittedModel:
    family: ModelFamily
    task: TaskKind
    parameter_names: tuple[str,...]
    parameter_values: tuple[float,...]
    feature_count: int

    def raw(self,x:tuple[float,...])->float:
        if len(x)!=self.feature_count:raise ValueError("model feature width mismatch")
        p=dict(zip(self.parameter_names,self.parameter_values))
        if self.family==ModelFamily.NEVER_TRADE:return -20.0
        if self.family==ModelFamily.ALWAYS_TRADE:return 20.0
        if self.family==ModelFamily.TRAIN_PREVALENCE:
            q=min(1-1e-12,max(1e-12,p["probability"]));return math.log(q/(1-q))
        if self.family in (ModelFamily.SINGLE_FEATURE_THRESHOLD,ModelFamily.DECISION_STUMP):
            idx=int(p["feature_index"]);direction=p["direction"];threshold=p["threshold"]
            high = x[idx]*direction >= threshold*direction
            q=p["high_probability"] if high else p["low_probability"]
            q=min(1-1e-12,max(1e-12,q));return math.log(q/(1-q))
        if self.family==ModelFamily.LOGISTIC_RIDGE:
            return p["intercept"]+sum(p[f"w_{i}"]*x[i] for i in range(self.feature_count))
        if self.family==ModelFamily.RIDGE_REGRESSION:
            return p["intercept"]+sum(p[f"w_{i}"]*x[i] for i in range(self.feature_count))
        raise ValueError("unsupported fitted model family")

    def probability(self,x:tuple[float,...])->float:
        return sigmoid(self.raw(x)) if self.task==TaskKind.BINARY_CLASSIFICATION else self.raw(x)

def fit_never(feature_count:int,task:TaskKind)->FittedModel:
    return FittedModel(ModelFamily.NEVER_TRADE,task,(),(),feature_count)

def fit_always(feature_count:int,task:TaskKind)->FittedModel:
    return FittedModel(ModelFamily.ALWAYS_TRADE,task,(),(),feature_count)

def fit_prevalence(x,y,task:TaskKind)->FittedModel:
    if task!=TaskKind.BINARY_CLASSIFICATION:raise ValueError("prevalence is binary only")
    q=sum(y)/len(y)
    return FittedModel(ModelFamily.TRAIN_PREVALENCE,task,("probability",),(q,),len(x[0]))

def fit_threshold(x,y,task:TaskKind,grid_size:int=32,family:ModelFamily=ModelFamily.SINGLE_FEATURE_THRESHOLD)->FittedModel:
    if task!=TaskKind.BINARY_CLASSIFICATION:raise ValueError("threshold model is binary only")
    width=len(x[0]);best=None
    for feature in range(width):
        unique=sorted(set(row[feature] for row in x))
        if len(unique)>grid_size:
            positions=sorted(set(round(i*(len(unique)-1)/(grid_size-1)) for i in range(grid_size)))
            unique=[unique[i] for i in positions]
        thresholds=unique if len(unique)==1 else [(a+b)/2 for a,b in zip(unique,unique[1:])]
        for direction in (1.0,-1.0):
            for threshold in thresholds:
                groups=[row[feature]*direction>=threshold*direction for row in x]
                high=[target for target,g in zip(y,groups) if g];low=[target for target,g in zip(y,groups) if not g]
                hp=(sum(high)+1)/(len(high)+2);lp=(sum(low)+1)/(len(low)+2)
                loss=sum((target-(hp if group else lp))**2 for target,group in zip(y,groups))/len(y)
                key=(loss,feature,-direction,threshold)
                if best is None or key<best[0]:best=(key,feature,direction,threshold,lp,hp)
    _,feature,direction,threshold,lp,hp=best
    names=("feature_index","direction","threshold","low_probability","high_probability")
    return FittedModel(family,task,names,(float(feature),direction,threshold,lp,hp),width)

def fit_logistic_ridge(x,y,iterations:int=500,learning_rate:float=0.05,l2:float=0.01)->FittedModel:
    width=len(x[0]);weights=[0.0]*width;intercept=0.0;n=len(x)
    for step in range(iterations):
        grad=[0.0]*width;gi=0.0
        for row,target in zip(x,y):
            p=sigmoid(intercept+sum(w*v for w,v in zip(weights,row)));error=p-target;gi+=error
            for i,value in enumerate(row):grad[i]+=error*value
        rate=learning_rate/(1.0+0.001*step)
        intercept-=rate*gi/n
        for i in range(width):weights[i]-=rate*(grad[i]/n+l2*weights[i])
    names=("intercept",)+tuple(f"w_{i}" for i in range(width))
    return FittedModel(ModelFamily.LOGISTIC_RIDGE,TaskKind.BINARY_CLASSIFICATION,names,(intercept,*weights),width)

def fit_ridge_regression(x,y,iterations:int=500,learning_rate:float=0.03,l2:float=0.01)->FittedModel:
    width=len(x[0]);weights=[0.0]*width;intercept=sum(y)/len(y);n=len(x)
    for step in range(iterations):
        grad=[0.0]*width;gi=0.0
        for row,target in zip(x,y):
            error=intercept+sum(w*v for w,v in zip(weights,row))-target;gi+=error
            for i,value in enumerate(row):grad[i]+=error*value
        rate=learning_rate/(1.0+0.001*step);intercept-=rate*2*gi/n
        for i in range(width):weights[i]-=rate*(2*grad[i]/n+2*l2*weights[i])
    names=("intercept",)+tuple(f"w_{i}" for i in range(width))
    return FittedModel(ModelFamily.RIDGE_REGRESSION,TaskKind.REGRESSION,names,(intercept,*weights),width)
