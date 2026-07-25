from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType,MonotonicDirection
from .parameters import ParameterSpec,ParameterSchema
from .plans import TrailingPlan
D=Decimal
def S(a,*x): return ParameterSchema(f'{a}.params','1.0.0',tuple(x))
def P(n,t,d,mi=None,ma=None,u='unitless',m=MonotonicDirection.NONE): return ParameterSpec(n,t,d,mi,ma,units=u,monotonic_direction=m)
class NoTrail(AtomBase):
 descriptor=descriptor('trailing.none',TreatmentKind.TRAILING,'none',S('trailing.none'))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'none',D(0),None,None,0)
class BreakEvenTrail(AtomBase):
 descriptor=descriptor('trailing.break_even',TreatmentKind.TRAILING,'break_even',S('trailing.break_even',P('activation_r',ParameterType.DECIMAL,'1','0','100','R'),P('offset_points',ParameterType.DECIMAL,'0','0','100000','points')))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'break_even',i.parameters.get_decimal('activation_r'),c.price.points(i.parameters.get_decimal('offset_points')),D(0),0)
class ProfitLockTrail(AtomBase):
 descriptor=descriptor('trailing.profit_lock',TreatmentKind.TRAILING,'profit_lock',S('trailing.profit_lock',P('activation_r',ParameterType.DECIMAL,'1.5','0','100','R'),P('lock_r',ParameterType.DECIMAL,'0.5','0','100','R')))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'profit_lock',i.parameters.get_decimal('activation_r'),None,i.parameters.get_decimal('lock_r'),0)
class SwingNodeTrail(AtomBase):
 descriptor=descriptor('trailing.swing_node',TreatmentKind.TRAILING,'swing_node',S('trailing.swing_node',P('activation_r',ParameterType.DECIMAL,'1','0','100','R'),P('buffer_points',ParameterType.DECIMAL,'2','0','100000','points')),required=('swing_high','swing_low'))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'swing_node',i.parameters.get_decimal('activation_r'),c.price.points(i.parameters.get_decimal('buffer_points')),None,0,'swing_low' if c.side.value=='long' else 'swing_high')
class AtrTrail(AtomBase):
 descriptor=descriptor('trailing.atr',TreatmentKind.TRAILING,'volatility',S('trailing.atr',P('activation_r',ParameterType.DECIMAL,'1','0','100','R'),P('atr_multiple',ParameterType.DECIMAL,'2','0.05','100','multiple')),required=('atr',))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'atr',i.parameters.get_decimal('activation_r'),c.level('atr')*i.parameters.get_decimal('atr_multiple'),None,0,'atr')
class ChandelierTrail(AtomBase):
 descriptor=descriptor('trailing.chandelier',TreatmentKind.TRAILING,'chandelier',S('trailing.chandelier',P('activation_r',ParameterType.DECIMAL,'1','0','100','R'),P('atr_multiple',ParameterType.DECIMAL,'3','0.05','100','multiple')),required=('atr','swing_high','swing_low'))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'chandelier',i.parameters.get_decimal('activation_r'),c.level('atr')*i.parameters.get_decimal('atr_multiple'),None,0,'highest_since_entry' if c.side.value=='long' else 'lowest_since_entry')
class TimeStepTrail(AtomBase):
 descriptor=descriptor('trailing.time_step',TreatmentKind.TRAILING,'time_step',S('trailing.time_step',P('activation_r',ParameterType.DECIMAL,'0.5','0','100','R'),P('step_ms',ParameterType.INTEGER,300000,1,86400000,'milliseconds'),P('lock_increment_r',ParameterType.DECIMAL,'0.25','0','100','R')))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'time_step',i.parameters.get_decimal('activation_r'),None,i.parameters.get_decimal('lock_increment_r'),i.parameters.get_int('step_ms'))
class ContextStateTrail(AtomBase):
 descriptor=descriptor('trailing.context_state',TreatmentKind.TRAILING,'context_state',S('trailing.context_state',P('activation_r',ParameterType.DECIMAL,'0','0','100','R'),P('buffer_points',ParameterType.DECIMAL,'1','0','100000','points')),required=('context_high','context_low'))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'context_state',i.parameters.get_decimal('activation_r'),c.price.points(i.parameters.get_decimal('buffer_points')),None,0,'context_low' if c.side.value=='long' else 'context_high')
class OppositeSignalTrail(AtomBase):
 descriptor=descriptor('trailing.opposite_signal',TreatmentKind.TRAILING,'opposite_signal',S('trailing.opposite_signal',P('activation_r',ParameterType.DECIMAL,'0','0','100','R')))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'opposite_signal',i.parameters.get_decimal('activation_r'),None,None,0,'opposite_context_signal')
class ActivationConditionedTrail(AtomBase):
 descriptor=descriptor('trailing.activation_conditioned',TreatmentKind.TRAILING,'activation_conditioned',S('trailing.activation_conditioned',P('activation_r',ParameterType.DECIMAL,'2','0','100','R'),P('distance_points',ParameterType.DECIMAL,'50','0.1','1000000','points'),P('cadence_ms',ParameterType.INTEGER,1000,0,86400000,'milliseconds')))
 def build(self,c,i): return TrailingPlan(i.invocation_id,'activation_conditioned',i.parameters.get_decimal('activation_r'),c.price.points(i.parameters.get_decimal('distance_points')),None,i.parameters.get_int('cadence_ms'),'favorable_excursion')
TRAILING_ATOMS=(NoTrail,BreakEvenTrail,ProfitLockTrail,SwingNodeTrail,AtrTrail,ChandelierTrail,TimeStepTrail,ContextStateTrail,OppositeSignalTrail,ActivationConditionedTrail)
