from __future__ import annotations
from .errors import BudgetError
class BudgetLedger:
    def __init__(self,budget):self.budget=budget;self.counters={'contexts':0,'treatments':0,'scenarios':0,'objective_evaluations':0,'calibration_iterations':0,'pareto_points':0,'counterfactual_queries':0,'hidden_evaluation_queries':0,'protected_evidence_exposure':0,'failures':0}
    def consume(self,key,n=1):
        self.counters[key]=self.counters.get(key,0)+int(n)
        field='max_'+key
        limit=getattr(self.budget,field,None)
        if limit is not None and self.counters[key]>limit:raise BudgetError(f'budget exceeded: {key}')
        if key=='hidden_evaluation_queries' and self.counters[key]>0:raise BudgetError('hidden evaluation forbidden')
        if key=='protected_evidence_exposure' and self.counters[key]>0:raise BudgetError('protected evidence forbidden')
    def snapshot(self):return dict(self.counters)
