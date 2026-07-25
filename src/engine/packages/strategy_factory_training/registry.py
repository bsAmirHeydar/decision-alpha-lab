from __future__ import annotations
from dataclasses import dataclass
from typing import Protocol, Callable
from .enums import ModelFamily, TaskKind
from .baselines import *

class TrainerPlugin(Protocol):
    family: ModelFamily
    version: str
    task: TaskKind
    def fit(self,x,y,plan): ...

@dataclass(frozen=True,slots=True)
class FunctionTrainer:
    family: ModelFamily
    version: str
    task: TaskKind
    function: Callable
    def fit(self,x,y,plan):return self.function(x,y,plan)

class StaticTrainerRegistry:
    def __init__(self):self._plugins={}
    def register(self,plugin:TrainerPlugin)->None:
        key=(plugin.family,plugin.version,plugin.task)
        if key in self._plugins:raise ValueError("duplicate exact trainer registration")
        self._plugins[key]=plugin
    def resolve(self,family:ModelFamily,version:str,task:TaskKind)->TrainerPlugin:
        key=(family,version,task)
        if key not in self._plugins:raise KeyError(f"trainer not registered: {family.name}@{version}/{task.name}")
        return self._plugins[key]
    @property
    def registry_hash(self)->str:
        from .hashing import stable_id
        keys=sorted(f"{int(f)}|{v}|{int(t)}" for f,v,t in self._plugins)
        return stable_id("treg","||".join(keys))

def reference_registry()->StaticTrainerRegistry:
    registry=StaticTrainerRegistry()
    registry.register(FunctionTrainer(ModelFamily.NEVER_TRADE,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_never(len(x[0]),p.task)))
    registry.register(FunctionTrainer(ModelFamily.ALWAYS_TRADE,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_always(len(x[0]),p.task)))
    registry.register(FunctionTrainer(ModelFamily.TRAIN_PREVALENCE,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_prevalence(x,y,p.task)))
    registry.register(FunctionTrainer(ModelFamily.SINGLE_FEATURE_THRESHOLD,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_threshold(x,y,p.task,p.threshold_grid_size)))
    registry.register(FunctionTrainer(ModelFamily.DECISION_STUMP,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_threshold(x,y,p.task,p.threshold_grid_size,ModelFamily.DECISION_STUMP)))
    registry.register(FunctionTrainer(ModelFamily.LOGISTIC_RIDGE,"1.0.0",TaskKind.BINARY_CLASSIFICATION,lambda x,y,p:fit_logistic_ridge(x,y,p.maximum_iterations,p.learning_rate,p.l2_penalty)))
    registry.register(FunctionTrainer(ModelFamily.RIDGE_REGRESSION,"1.0.0",TaskKind.REGRESSION,lambda x,y,p:fit_ridge_regression(x,y,p.maximum_iterations,p.learning_rate,p.l2_penalty)))
    return registry
