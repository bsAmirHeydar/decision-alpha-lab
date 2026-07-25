from __future__ import annotations
from dataclasses import dataclass
from .models import CostBreakdown
from .hashing import stable_id

@dataclass(frozen=True,slots=True)
class CostRequest:
    candidate_id:str; initial_risk_points:float; observed_entry_spread_points:float=0.0; observed_exit_spread_points:float=0.0

class FixedCostModel:
    def __init__(self,model_id="sf09.cost.fixed",version="1.0.0",use_observed_spread=True,entry_spread=0.0,exit_spread=0.0,entry_slippage=0.0,exit_slippage=0.0,commission_r=0.0,other_r=0.0):
        self.model_id=model_id;self.version=version;self.use_observed_spread=use_observed_spread;self.entry_spread=entry_spread;self.exit_spread=exit_spread;self.entry_slippage=entry_slippage;self.exit_slippage=exit_slippage;self.commission_r=commission_r;self.other_r=other_r
    @property
    def descriptor_hash(self):return stable_id("cmdl",f"{self.model_id}|{self.version}|{str(self.use_observed_spread).lower()}")
    def compute(self,r:CostRequest)->CostBreakdown:
        if r.initial_risk_points<=0:raise ValueError("invalid risk")
        es=r.observed_entry_spread_points if self.use_observed_spread else self.entry_spread
        xs=r.observed_exit_spread_points if self.use_observed_spread else self.exit_spread
        pts=max(0,es)+max(0,xs)+self.entry_slippage+self.exit_slippage
        total_r=pts/r.initial_risk_points+self.commission_r+self.other_r
        return CostBreakdown(self.model_id,self.version,max(0,es),max(0,xs),self.entry_slippage,self.exit_slippage,self.commission_r,self.other_r,pts,total_r)

class CostRegistry:
    def __init__(self):self._items={};self._compiled=False;self.registry_hash=""
    def register(self,m):
        if self._compiled:raise RuntimeError("compiled")
        k=(m.model_id,m.version)
        if k in self._items:raise ValueError("duplicate cost model")
        self._items[k]=m
    def compile(self):
        if not self._items:raise ValueError("empty registry")
        self.registry_hash=stable_id("creg","".join(f"{k[0]}@{k[1]}|{self._items[k].descriptor_hash};" for k in sorted(self._items)))
        self._compiled=True;return self
    def resolve(self,model_id,version):
        if not self._compiled:raise RuntimeError("not compiled")
        return self._items[(model_id,version)]
