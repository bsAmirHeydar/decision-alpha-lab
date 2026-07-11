from __future__ import annotations
from dataclasses import dataclass
from .generation import RuntimeGeneration
from .enums import GenerationState
@dataclass(slots=True)
class GenerationBundle:
    generation:RuntimeGeneration; payload:object=None
class GenerationManager:
    def __init__(self):self.staged=None;self.active=None;self.previous=None;self.activation_count=0;self.rollback_count=0
    def stage(self,bundle:GenerationBundle):
        if bundle.generation.state is not GenerationState.WARMED:raise ValueError('only WARMED may be staged')
        self.staged=bundle
    def activate(self,now_utc_msc:int):
        if self.staged is None:raise ValueError('no staged generation')
        self.staged.generation=self.staged.generation.transition(GenerationState.ACTIVE,now_utc_msc)
        self.previous,self.active,self.staged=self.active,self.staged,None;self.activation_count+=1
        return self.active
    def rollback(self,now_utc_msc:int):
        if self.previous is None:raise ValueError('no previous generation')
        if self.active and self.active.generation.state is GenerationState.ACTIVE:self.active.generation=self.active.generation.transition(GenerationState.RETIRED,now_utc_msc)
        self.active,self.previous=self.previous,self.active
        if self.active.generation.state is GenerationState.RETIRED:
            from dataclasses import replace
            self.active.generation=replace(self.active.generation,state=GenerationState.WARMED).transition(GenerationState.ACTIVE,now_utc_msc)
        self.rollback_count+=1;return self.active
