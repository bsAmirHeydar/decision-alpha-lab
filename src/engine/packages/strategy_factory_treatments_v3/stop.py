from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType,TradeSide,PriceRole,MonotonicDirection
from .parameters import ParameterSpec,ParameterSchema
from .plans import StopPlan
from .utils import require
D=Decimal
def S(a,*x): return ParameterSchema(f'{a}.params','1.0.0',tuple(x))
def P(n,t,d,mi=None,ma=None,u='unitless',m=MonotonicDirection.NONE): return ParameterSpec(n,t,d,mi,ma,units=u,monotonic_direction=m)
def stop_from_level(c,level,buffer_points):
 b=c.price.points(buffer_points); raw=level-b if c.side is TradeSide.LONG else level+b; return c.price.conservative(raw,c.side,PriceRole.STOP)
def validate(c,p):
 e=c.price.executable_entry(c.side); require(p<e if c.side is TradeSide.LONG else p>e,'invalid_stop_side','stop must be protective relative to executable entry'); return abs(e-p)
class FixedDistanceStop(AtomBase):
 descriptor=descriptor('stop.fixed_distance',TreatmentKind.STOP,'fixed',S('stop.fixed_distance',P('distance_points',ParameterType.DECIMAL,'100','1','1000000','points',MonotonicDirection.INCREASING)))
 def build(self,c,i):
  e=c.price.executable_entry(c.side); d=c.price.points(i.parameters.get_decimal('distance_points')); p=c.price.conservative(e-d if c.side is TradeSide.LONG else e+d,c.side,PriceRole.STOP); return StopPlan(i.invocation_id,p,validate(c,p))
class StructuralStop(AtomBase):
 descriptor=descriptor('stop.structural',TreatmentKind.STOP,'structural',S('stop.structural',P('buffer_points',ParameterType.DECIMAL,'2','0','100000','points')),required=('structural_stop',))
 def build(self,c,i):
  p=stop_from_level(c,c.level('structural_stop'),i.parameters.get_decimal('buffer_points')); return StopPlan(i.invocation_id,p,validate(c,p))
class SignalBarStop(AtomBase):
 descriptor=descriptor('stop.signal_bar',TreatmentKind.STOP,'signal_bar',S('stop.signal_bar',P('buffer_points',ParameterType.DECIMAL,'1','0','100000','points')),required=('signal_high','signal_low'))
 def build(self,c,i):
  lvl=c.level('signal_low') if c.side is TradeSide.LONG else c.level('signal_high'); p=stop_from_level(c,lvl,i.parameters.get_decimal('buffer_points')); return StopPlan(i.invocation_id,p,validate(c,p))
class ContextBoundaryStop(AtomBase):
 descriptor=descriptor('stop.context_boundary',TreatmentKind.STOP,'context_boundary',S('stop.context_boundary',P('buffer_points',ParameterType.DECIMAL,'2','0','100000','points')),required=('context_high','context_low'))
 def build(self,c,i):
  lvl=c.level('context_low') if c.side is TradeSide.LONG else c.level('context_high'); p=stop_from_level(c,lvl,i.parameters.get_decimal('buffer_points')); return StopPlan(i.invocation_id,p,validate(c,p))
class VolatilityStop(AtomBase):
 descriptor=descriptor('stop.volatility',TreatmentKind.STOP,'volatility',S('stop.volatility',P('atr_multiple',ParameterType.DECIMAL,'1.5','0.05','50','multiple',MonotonicDirection.INCREASING),P('minimum_points',ParameterType.DECIMAL,'10','0','100000','points')),required=('atr',))
 def build(self,c,i):
  e=c.price.executable_entry(c.side); d=max(c.level('atr')*i.parameters.get_decimal('atr_multiple'),c.price.points(i.parameters.get_decimal('minimum_points'))); p=c.price.conservative(e-d if c.side is TradeSide.LONG else e+d,c.side,PriceRole.STOP); return StopPlan(i.invocation_id,p,validate(c,p))
class CatastrophicStop(AtomBase):
 descriptor=descriptor('stop.catastrophic',TreatmentKind.STOP,'catastrophic',S('stop.catastrophic',P('distance_points',ParameterType.DECIMAL,'500','1','10000000','points',MonotonicDirection.INCREASING)))
 def build(self,c,i):
  e=c.price.executable_entry(c.side); d=c.price.points(i.parameters.get_decimal('distance_points')); p=c.price.conservative(e-d if c.side is TradeSide.LONG else e+d,c.side,PriceRole.STOP); return StopPlan(i.invocation_id,p,validate(c,p),catastrophic_price=p,metadata={'role':'catastrophic_cap'})
class TimeStop(AtomBase):
 descriptor=descriptor('stop.time',TreatmentKind.STOP,'time',S('stop.time',P('holding_ms',ParameterType.INTEGER,3600000,1,604800000,'milliseconds')))
 def build(self,c,i): return StopPlan(i.invocation_id,None,None,time_exit_ms=c.decision_time_ms+i.parameters.get_int('holding_ms'),metadata={'price_stop':'absent'})
class HybridStop(AtomBase):
 descriptor=descriptor('stop.hybrid',TreatmentKind.STOP,'hybrid',S('stop.hybrid',P('buffer_points',ParameterType.DECIMAL,'2','0','100000','points'),P('max_distance_points',ParameterType.DECIMAL,'250','1','1000000','points')),required=('structural_stop',))
 def build(self,c,i):
  e=c.price.executable_entry(c.side); structural=stop_from_level(c,c.level('structural_stop'),i.parameters.get_decimal('buffer_points')); cap=c.price.points(i.parameters.get_decimal('max_distance_points')); capped=e-cap if c.side is TradeSide.LONG else e+cap; raw=max(structural,capped) if c.side is TradeSide.LONG else min(structural,capped); p=c.price.conservative(raw,c.side,PriceRole.STOP); return StopPlan(i.invocation_id,p,validate(c,p),metadata={'selection':'structural_capped_by_max_distance'})
STOP_ATOMS=(FixedDistanceStop,StructuralStop,SignalBarStop,ContextBoundaryStop,VolatilityStop,CatastrophicStop,TimeStop,HybridStop)
