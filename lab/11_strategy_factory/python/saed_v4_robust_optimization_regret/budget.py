from __future__ import annotations
from dataclasses import dataclass
from .contracts import OptimizationBudget
from .errors import BudgetError
from .canonical import content_hash

@dataclass
class BudgetLedger:
    contract:OptimizationBudget
    candidates:int=0;scenarios:int=0;ambiguity_distributions:int=0;allocations:int=0;objective_evaluations:int=0;adversarial_steps:int=0;stability_resamples:int=0;hidden_evaluation_queries:int=0;protected_evidence_exposures:int=0;failures:int=0
    def consume(self,field,amount=1):
        if amount<0: raise BudgetError('negative budget consumption')
        setattr(self,field,getattr(self,field)+int(amount))
        limit_name={'candidates':'max_candidates','scenarios':'max_scenarios','ambiguity_distributions':'max_ambiguity_distributions','allocations':'max_allocations','objective_evaluations':'max_objective_evaluations','adversarial_steps':'max_adversarial_steps','stability_resamples':'max_stability_resamples','hidden_evaluation_queries':'max_hidden_evaluation_queries','protected_evidence_exposures':'protected_evidence_exposure_limit','failures':'max_failures'}[field]
        if getattr(self,field)>getattr(self.contract,limit_name): raise BudgetError(f'budget exceeded: {field}')
    def snapshot(self):
        d={'candidates':self.candidates,'scenarios':self.scenarios,'ambiguity_distributions':self.ambiguity_distributions,'allocations':self.allocations,'objective_evaluations':self.objective_evaluations,'adversarial_steps':self.adversarial_steps,'stability_resamples':self.stability_resamples,'hidden_evaluation_queries':self.hidden_evaluation_queries,'protected_evidence_exposures':self.protected_evidence_exposures,'failures':self.failures,'limits':self.contract.__dict__}
        d['ledger_hash']=content_hash(d);return d
