from __future__ import annotations
from .errors import BudgetError
class ExposureLedger:
    def __init__(self,budget):self.budget=budget;self.counts={'facts':0,'rules':0,'inferences':0,'counterexamples':0,'synthesis_candidates':0,'symbolic_terms':0,'neural_queries':0,'hidden_evaluation_queries':0,'protected_evidence_exposures':0,'failures':0}
    def add(self,key,n=1):
        if key not in self.counts:raise BudgetError('unknown ledger key')
        self.counts[key]+=int(n)
        cap={'facts':'max_facts','rules':'max_rules','inferences':'max_inferences','counterexamples':'max_counterexamples','synthesis_candidates':'max_synthesis_candidates','symbolic_terms':'max_symbolic_terms','neural_queries':'max_neural_queries','hidden_evaluation_queries':'max_hidden_evaluation_queries','protected_evidence_exposures':'protected_evidence_exposure_limit','failures':'max_failures'}[key]
        if self.counts[key]>getattr(self.budget,cap):raise BudgetError(f'{key} budget exhausted')
    def snapshot(self):return {'counts':dict(self.counts),'limits':self.budget.__dict__.copy(),'within_budget':True}
