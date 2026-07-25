from __future__ import annotations
from dataclasses import dataclass
from .models import PassSummary
from .enums import PassStatus
@dataclass(frozen=True,slots=True)
class SelectionPolicy: maximum_passes:int=20; minimum_score:float=-1e99; minimum_expectancy_r:float=0.0; minimum_unique_events:int=30
class SelectedPassCollector:
    def __init__(self,policy:SelectionPolicy): self.policy=policy; self.items=[]
    def consider(self,s:PassSummary)->bool:
        if s.status!=PassStatus.VALID or s.objective_score<self.policy.minimum_score or s.metrics.expectancy_r<self.policy.minimum_expectancy_r or s.metrics.unique_event_count<self.policy.minimum_unique_events:return False
        self.items.append(s);self.items.sort(key=lambda x:x.objective_score,reverse=True);del self.items[self.policy.maximum_passes:];return True
