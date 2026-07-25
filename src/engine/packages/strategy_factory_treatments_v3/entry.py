from __future__ import annotations
from decimal import Decimal
from .atom_base import AtomBase
from .descriptor_factory import descriptor
from .enums import TreatmentKind,ParameterType,EntryOrderType,TradeSide,PriceRole,MonotonicDirection
from .parameters import ParameterSpec,ParameterSchema
from .plans import EntryPlan,EntryLeg
from .utils import dec,require
D=Decimal

def S(atom,*specs): return ParameterSchema(f'{atom}.params','1.0.0',tuple(specs))
def P(n,t,d,mi=None,ma=None,u='unitless',m=MonotonicDirection.NONE,desc=''): return ParameterSpec(n,t,d,mi,ma,units=u,monotonic_direction=m,description=desc)
class ImmediateMarketEntry(AtomBase):
 descriptor=descriptor('entry.immediate_market',TreatmentKind.ENTRY,'immediate',S('entry.immediate_market',P('max_age_ms',ParameterType.INTEGER,1000,0,60000,'milliseconds')))
 def build(self,c,i):
  require(c.decision_time_ms-c.price.quote_time_ms<=i.parameters.get_int('max_age_ms'),'stale_quote','market entry quote is stale')
  p=c.price.round_tick(c.price.executable_entry(c.side)); return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.MARKET,p,D(1),c.decision_time_ms,c.decision_time_ms),),metadata={'executable_side':'ask' if c.side is TradeSide.LONG else 'bid'})
class PassiveLimitEntry(AtomBase):
 descriptor=descriptor('entry.passive_limit',TreatmentKind.ENTRY,'passive',S('entry.passive_limit',P('offset_points',ParameterType.DECIMAL,'10','0','100000','points',MonotonicDirection.INCREASING),P('ttl_ms',ParameterType.INTEGER,300000,1,86400000,'milliseconds')))
 def build(self,c,i):
  off=c.price.points(i.parameters.get_decimal('offset_points')); raw=c.price.ask-off if c.side is TradeSide.LONG else c.price.bid+off; p=c.price.round_tick(raw); c.price.validate_pending(c.side,'limit',p)
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.LIMIT,p,D(1),c.decision_time_ms,c.decision_time_ms+i.parameters.get_int('ttl_ms'),p),))
class BreakoutStopEntry(AtomBase):
 descriptor=descriptor('entry.breakout_stop',TreatmentKind.ENTRY,'breakout',S('entry.breakout_stop',P('buffer_points',ParameterType.DECIMAL,'2','0','10000','points'),P('ttl_ms',ParameterType.INTEGER,300000,1,86400000,'milliseconds')),required=('reference_price',))
 def build(self,c,i):
  buf=c.price.points(i.parameters.get_decimal('buffer_points')); raw=c.level('reference_price')+buf if c.side is TradeSide.LONG else c.level('reference_price')-buf; p=c.price.round_tick(raw); c.price.validate_pending(c.side,'stop',p)
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.STOP,p,D(1),c.decision_time_ms,c.decision_time_ms+i.parameters.get_int('ttl_ms')),))
class ConfirmationMarketEntry(AtomBase):
 descriptor=descriptor('entry.confirmation_market',TreatmentKind.ENTRY,'confirmation',S('entry.confirmation_market',P('max_deviation_points',ParameterType.DECIMAL,'20','0','100000','points')),required=('confirmation_price',))
 def build(self,c,i):
  p=c.price.round_tick(c.price.executable_entry(c.side)); dev=abs(p-c.level('confirmation_price'))
  require(dev<=c.price.points(i.parameters.get_decimal('max_deviation_points')),'confirmation_deviation','executable price too far from confirmation')
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.MARKET,p,D(1),c.decision_time_ms,c.decision_time_ms),),metadata={'confirmation_price':str(c.confirmation_price)})
class RetestLimitEntry(AtomBase):
 descriptor=descriptor('entry.retest_limit',TreatmentKind.ENTRY,'retest',S('entry.retest_limit',P('offset_points',ParameterType.DECIMAL,'0','0','10000','points'),P('ttl_ms',ParameterType.INTEGER,600000,1,86400000,'milliseconds')),required=('retest_price',))
 def build(self,c,i):
  off=c.price.points(i.parameters.get_decimal('offset_points')); raw=c.level('retest_price')-off if c.side is TradeSide.LONG else c.level('retest_price')+off; p=c.price.round_tick(raw); c.price.validate_pending(c.side,'limit',p)
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.LIMIT,p,D(1),c.decision_time_ms,c.decision_time_ms+i.parameters.get_int('ttl_ms'),p),))
class LadderEntry(AtomBase):
 descriptor=descriptor('entry.ladder',TreatmentKind.ENTRY,'ladder',S('entry.ladder',P('leg_count',ParameterType.INTEGER,3,2,8,'count'),P('spacing_points',ParameterType.DECIMAL,'10','0.1','100000','points'),P('ttl_ms',ParameterType.INTEGER,900000,1,86400000,'milliseconds')))
 def build(self,c,i):
  n=i.parameters.get_int('leg_count'); spacing=c.price.points(i.parameters.get_decimal('spacing_points')); f=D(1)/D(n); legs=[]
  for k in range(n):
   raw=c.price.ask-spacing*D(k+1) if c.side is TradeSide.LONG else c.price.bid+spacing*D(k+1); p=c.price.round_tick(raw); c.price.validate_pending(c.side,'limit',p); legs.append(EntryLeg(EntryOrderType.LIMIT,p,f,c.decision_time_ms,c.decision_time_ms+i.parameters.get_int('ttl_ms'),p))
  return EntryPlan(i.invocation_id,tuple(legs),metadata={'normalization':'equal_weight'})
class StopLimitHybridEntry(AtomBase):
 descriptor=descriptor('entry.stop_limit_hybrid',TreatmentKind.ENTRY,'hybrid',S('entry.stop_limit_hybrid',P('trigger_buffer_points',ParameterType.DECIMAL,'2','0','10000','points'),P('limit_slip_points',ParameterType.DECIMAL,'5','0','10000','points'),P('ttl_ms',ParameterType.INTEGER,300000,1,86400000,'milliseconds')),required=('reference_price',))
 def build(self,c,i):
  b=c.price.points(i.parameters.get_decimal('trigger_buffer_points')); s=c.price.points(i.parameters.get_decimal('limit_slip_points')); trig=c.level('reference_price')+b if c.side is TradeSide.LONG else c.level('reference_price')-b; trig=c.price.round_tick(trig); c.price.validate_pending(c.side,'stop',trig); lim=trig+s if c.side is TradeSide.LONG else trig-s; lim=c.price.round_tick(lim)
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.STOP_LIMIT,trig,D(1),c.decision_time_ms,c.decision_time_ms+i.parameters.get_int('ttl_ms'),lim),))
class TimeWindowEntry(AtomBase):
 descriptor=descriptor('entry.time_window',TreatmentKind.ENTRY,'time_window',S('entry.time_window',P('delay_ms',ParameterType.INTEGER,0,0,86400000,'milliseconds'),P('window_ms',ParameterType.INTEGER,60000,1,86400000,'milliseconds')))
 def build(self,c,i):
  a=c.decision_time_ms+i.parameters.get_int('delay_ms'); z=a+i.parameters.get_int('window_ms'); p=c.price.round_tick(c.price.executable_entry(c.side))
  return EntryPlan(i.invocation_id,(EntryLeg(EntryOrderType.MARKET,p,D(1),a,z),),cancel_policy='expire_at_window_end')
ENTRY_ATOMS=(ImmediateMarketEntry,PassiveLimitEntry,BreakoutStopEntry,ConfirmationMarketEntry,RetestLimitEntry,LadderEntry,StopLimitHybridEntry,TimeWindowEntry)
