from __future__ import annotations
from dataclasses import dataclass
from .models import ReferenceState
@dataclass
class ReferenceStateMachine:
 state:ReferenceState=ReferenceState.UNTOUCHED_BOTH
 hunter_symbol:str|None=None
 protected_symbol:str|None=None
 def first_touch(self,hunter:str,protected:str):
  if self.state==ReferenceState.UNTOUCHED_BOTH:self.state=ReferenceState.ONE_SIDE_TOUCHED;self.hunter_symbol=hunter;self.protected_symbol=protected
  return self.state
 def confirm(self):
  if self.state==ReferenceState.ONE_SIDE_TOUCHED:self.state=ReferenceState.DIVERGENCE_CONFIRMED
  return self.state
 def protected_touch(self):
  if self.state==ReferenceState.ONE_SIDE_TOUCHED:self.state=ReferenceState.BOTH_SIDES_TOUCHED
  elif self.state==ReferenceState.DIVERGENCE_CONFIRMED:self.state=ReferenceState.REFERENCE_EXHAUSTED
  return self.state
