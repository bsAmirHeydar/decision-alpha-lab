from __future__ import annotations
from dataclasses import asdict
from .canonical import content_hash, stable_id
from .contracts import ResearchBudget
from .errors import BudgetError
class ResearchLedger:
    def __init__(self,budget:ResearchBudget):
        self.budget=budget
        self.counts={k.removeprefix("maximum_"):0 for k in asdict(budget) if k.startswith("maximum_")}
        self.trials=[]
    def consume(self,name:str,count:int=1,metadata=None):
        if name not in self.counts: raise BudgetError(f"unknown budget counter {name}")
        self.counts[name]+=count
        maximum=getattr(self.budget,f"maximum_{name}")
        if self.counts[name]>maximum: raise BudgetError(f"budget exceeded for {name}")
        if metadata is not None: self.trials.append({"family":name,"count":count,"metadata":metadata})
    def snapshot(self):
        maxima={k.removeprefix("maximum_"):v for k,v in asdict(self.budget).items() if k.startswith("maximum_")}
        value={"phase":"SAED_V4_26","counts":dict(sorted(self.counts.items())),"maxima":dict(sorted(maxima.items())),"within_budget":all(self.counts[k]<=maxima[k] for k in self.counts),"complete":True}
        value["budget_snapshot_id"]=stable_id("mechanistic_budget",value); value["budget_snapshot_hash"]=content_hash(value)
        return value
    def trial_ledger(self):
        value={"phase":"SAED_V4_26","entries":self.trials,"complete":True,"trial_family_count":len(self.trials)}
        value["trial_ledger_id"]=stable_id("mechanistic_trial_ledger",value); value["trial_ledger_hash"]=content_hash(value)
        return value
