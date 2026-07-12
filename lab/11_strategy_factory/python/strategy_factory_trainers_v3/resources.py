from dataclasses import dataclass
from time import monotonic
from .errors import ResourceBudgetError
class CancellationToken:
 def __init__(self):self.cancelled=False;self.reason=''
 def cancel(self,reason='operator_cancelled'):self.cancelled=True;self.reason=reason
 def require_active(self):
  if self.cancelled:raise ResourceBudgetError('training_cancelled',self.reason)
@dataclass(slots=True)
class BudgetGuard:
 budget:object;schema:object;token:CancellationToken;started:float=0.;checkpoints:int=0
 def start(self):
  if self.schema.row_count>self.budget.max_rows:raise ResourceBudgetError('row_budget_exceeded','row budget')
  estimated=self.schema.row_count*len(self.schema.feature_order)*8/1024/1024
  if estimated>self.budget.max_memory_mb:raise ResourceBudgetError('memory_budget_exceeded','memory budget')
  self.started=monotonic();self.token.require_active()
 def poll(self):
  self.token.require_active()
  if monotonic()-self.started>self.budget.max_wall_seconds:raise ResourceBudgetError('training_timed_out','timeout')
 @property
 def elapsed_ms(self):return int((monotonic()-self.started)*1000) if self.started else 0
