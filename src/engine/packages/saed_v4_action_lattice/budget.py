from __future__ import annotations
from dataclasses import dataclass
from .errors import BudgetError
from .models import SolverBudget

@dataclass
class BudgetMeter:
    budget:SolverBudget
    candidates:int=0
    constraint_evaluations:int=0
    nodes:int=0
    edges:int=0
    operations:int=0
    def _guard(self,value:int,limit:int,label:str)->None:
        if value>limit: raise BudgetError(f'{label} budget exceeded: {value}>{limit}')
    def add_candidate(self,n:int=1): self.candidates+=n;self.operations+=n;self._guard(self.candidates,self.budget.maximum_candidates,'candidate');self._guard(self.operations,self.budget.operation_budget,'operation')
    def add_constraints(self,n:int): self.constraint_evaluations+=n;self.operations+=n;self._guard(self.constraint_evaluations,self.budget.maximum_constraint_evaluations,'constraint evaluation');self._guard(self.operations,self.budget.operation_budget,'operation')
    def set_nodes(self,n:int): self.nodes=n;self._guard(n,self.budget.maximum_feasible_nodes,'node')
    def set_edges(self,n:int): self.edges=n;self._guard(n,self.budget.maximum_edges,'edge')
    def to_dict(self)->dict:
        return {'candidates_enumerated':self.candidates,'constraint_evaluations':self.constraint_evaluations,'feasible_nodes':self.nodes,'edges_emitted':self.edges,'deterministic_operations':self.operations,'wall_clock_ms_observed':None,'budget_enforcement':'deterministic_count_based','limits':self.budget.__dict__}
