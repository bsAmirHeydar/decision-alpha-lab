from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType,TradeSide,PriceRole,MonotonicDirection
from .parameters import ParameterSpec,ParameterSchema
from .plans import TargetPlan,TargetLeg
from .utils import require
D=Decimal
def S(a,*x): return ParameterSchema(f'{a}.params','1.0.0',tuple(x))
def P(n,t,d,mi=None,ma=None,u='unitless',m=MonotonicDirection.NONE): return ParameterSpec(n,t,d,mi,ma,units=u,monotonic_direction=m)
def fixed(c,d):
 e=c.price.executable_entry(c.side); raw=e+d if c.side is TradeSide.LONG else e-d; return c.price.conservative(raw,c.side,PriceRole.TARGET)
def validate(c,p):
 e=c.price.executable_entry(c.side); require(p>e if c.side is TradeSide.LONG else p<e,'invalid_target_side','target must be favorable relative to entry')
class FixedRTarget(AtomBase):
 descriptor=descriptor('target.fixed_r',TreatmentKind.TARGET,'fixed_r',S('target.fixed_r',P('reward_multiple',ParameterType.DECIMAL,'2','0.05','100','R',MonotonicDirection.INCREASING),P('risk_points',ParameterType.DECIMAL,'100','0.1','1000000','points')))
 def build(self,c,i):
  p=fixed(c,c.price.points(i.parameters.get_decimal('risk_points'))*i.parameters.get_decimal('reward_multiple')); validate(c,p); return TargetPlan(i.invocation_id,(TargetLeg(p,D(1)),))
class StructuralTarget(AtomBase):
 descriptor=descriptor('target.structural',TreatmentKind.TARGET,'structural',S('target.structural',P('buffer_points',ParameterType.DECIMAL,'0','0','100000','points')),required=('structural_target',))
 def build(self,c,i):
  b=c.price.points(i.parameters.get_decimal('buffer_points')); raw=c.level('structural_target')-b if c.side is TradeSide.LONG else c.level('structural_target')+b; p=c.price.conservative(raw,c.side,PriceRole.TARGET); validate(c,p); return TargetPlan(i.invocation_id,(TargetLeg(p,D(1)),))
class ContextEndpointTarget(AtomBase):
 descriptor=descriptor('target.context_endpoint',TreatmentKind.TARGET,'context_endpoint',S('target.context_endpoint',P('buffer_points',ParameterType.DECIMAL,'0','0','100000','points')),required=('context_high','context_low'))
 def build(self,c,i):
  lvl=c.level('context_high') if c.side is TradeSide.LONG else c.level('context_low'); b=c.price.points(i.parameters.get_decimal('buffer_points')); raw=lvl-b if c.side is TradeSide.LONG else lvl+b; p=c.price.conservative(raw,c.side,PriceRole.TARGET); validate(c,p); return TargetPlan(i.invocation_id,(TargetLeg(p,D(1)),))
class VolatilityTarget(AtomBase):
 descriptor=descriptor('target.volatility',TreatmentKind.TARGET,'volatility',S('target.volatility',P('atr_multiple',ParameterType.DECIMAL,'2','0.05','100','multiple',MonotonicDirection.INCREASING)),required=('atr',))
 def build(self,c,i):
  p=fixed(c,c.level('atr')*i.parameters.get_decimal('atr_multiple')); validate(c,p); return TargetPlan(i.invocation_id,(TargetLeg(p,D(1)),))
class MultiTargetLadder(AtomBase):
 descriptor=descriptor('target.multi_ladder',TreatmentKind.TARGET,'ladder',S('target.multi_ladder',P('first_r',ParameterType.DECIMAL,'1','0.05','100','R'),P('step_r',ParameterType.DECIMAL,'1','0.05','100','R'),P('leg_count',ParameterType.INTEGER,3,2,8,'count'),P('risk_points',ParameterType.DECIMAL,'100','0.1','1000000','points')))
 def build(self,c,i):
  n=i.parameters.get_int('leg_count'); risk=c.price.points(i.parameters.get_decimal('risk_points')); first=i.parameters.get_decimal('first_r'); step=i.parameters.get_decimal('step_r'); f=D(1)/D(n); legs=[]
  for k in range(n):
   r=first+step*D(k); p=fixed(c,risk*r); validate(c,p); legs.append(TargetLeg(p,f,r))
  return TargetPlan(i.invocation_id,tuple(legs))
class RunnerTarget(AtomBase):
 descriptor=descriptor('target.runner',TreatmentKind.TARGET,'runner',S('target.runner',P('runner_fraction',ParameterType.DECIMAL,'1','0.01','1','fraction')))
 def build(self,c,i): return TargetPlan(i.invocation_id,(TargetLeg(None,i.parameters.get_decimal('runner_fraction'),None,True),),True)
class CappedRunnerTarget(AtomBase):
 descriptor=descriptor('target.capped_runner',TreatmentKind.TARGET,'runner',S('target.capped_runner',P('cap_r',ParameterType.DECIMAL,'8','0.1','1000','R'),P('risk_points',ParameterType.DECIMAL,'100','0.1','1000000','points')))
 def build(self,c,i):
  p=fixed(c,c.price.points(i.parameters.get_decimal('risk_points'))*i.parameters.get_decimal('cap_r')); validate(c,p); return TargetPlan(i.invocation_id,(TargetLeg(p,D(1),i.parameters.get_decimal('cap_r'),True),),False,{'runner':'open_until_cap_or_management_exit'})
TARGET_ATOMS=(FixedRTarget,StructuralTarget,ContextEndpointTarget,VolatilityTarget,MultiTargetLadder,RunnerTarget,CappedRunnerTarget)
