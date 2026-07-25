from __future__ import annotations
from .models import *
from .interfaces import *
from .enums import *
from .registry import PolicyRegistry
from .matrix import CandidateMatrixPlan

def _feature(s,name):
    if name not in s.values:raise KeyError(name)
    return float(s.values[name])
class ConfirmationMarket:
    descriptor=PolicyDescriptor("sf08.entry.confirmation_market","1.0.0",PolicyKind.ENTRY,required_feature_ids=("confirmation_price",))
    def admissible(self,e,s,f,p):return (PolicyDecision.ADMIT,"") if "confirmation_price" in s.values else (PolicyDecision.SKIP,"confirmation_price missing")
    def build(self,e,s,f,p):return EntryPlan(OrderKind.MARKET,_feature(s,"confirmation_price"),e.confirmation_time_ms,e.confirmation_time_ms+max(0,p.integers[0]),max(0,p.integers[0]),max(0.0,p.numeric[0]))
class ReferenceLimit:
    descriptor=PolicyDescriptor("sf08.entry.reference_limit","1.0.0",PolicyKind.ENTRY,requires_reference_price=True)
    def admissible(self,e,s,f,p):return (PolicyDecision.ADMIT,"") if e.reference_price>0 else (PolicyDecision.SKIP,"reference unavailable")
    def build(self,e,s,f,p):return EntryPlan(OrderKind.LIMIT,e.reference_price,e.confirmation_time_ms,e.confirmation_time_ms+max(1,p.integers[0]),max(1,p.integers[0]),max(0.0,p.numeric[0]))
class AnatomyStop:
    descriptor=PolicyDescriptor("sf08.stop.anatomy_invalidation","1.0.0",PolicyKind.STOP,requires_invalidation_price=True,required_feature_ids=("confirmation_price",))
    def admissible(self,e,s,f,p):return (PolicyDecision.ADMIT,"") if e.invalidation_price>0 and "confirmation_price" in s.values else (PolicyDecision.SKIP,"invalidation unavailable")
    def build(self,e,s,f,p):
        entry=_feature(s,"confirmation_price");return StopPlan(e.invalidation_price,abs(entry-e.invalidation_price))
class BufferedStop:
    descriptor=PolicyDescriptor("sf08.stop.buffered_invalidation","1.0.0",PolicyKind.STOP,requires_invalidation_price=True,required_feature_ids=("confirmation_price",))
    def admissible(self,e,s,f,p):return (PolicyDecision.ERROR,"negative buffer") if p.numeric[0]<0 else ((PolicyDecision.ADMIT,"") if "confirmation_price" in s.values else (PolicyDecision.SKIP,"confirmation missing"))
    def build(self,e,s,f,p):
        entry=_feature(s,"confirmation_price");sp=e.invalidation_price-p.numeric[0] if e.direction==1 else e.invalidation_price+p.numeric[0];return StopPlan(sp,abs(entry-sp))
class FixedR:
    descriptor=PolicyDescriptor("sf08.exit.fixed_r","1.0.0",PolicyKind.EXIT,requires_invalidation_price=True,required_feature_ids=("confirmation_price",))
    def admissible(self,e,s,f,p):return (PolicyDecision.ERROR,"R must be positive") if p.numeric[0]<=0 else ((PolicyDecision.ADMIT,"") if "confirmation_price" in s.values else (PolicyDecision.SKIP,"confirmation missing"))
    def build(self,e,s,f,p):
        entry=_feature(s,"confirmation_price");reward=abs(entry-e.invalidation_price)*p.numeric[0];target=entry+reward if e.direction==1 else entry-reward;kind=ExitKind.PRICE_OR_TIME if p.integers[0]>0 else ExitKind.PRICE_TARGET;return ExitPlan(kind,target,reward,True,max(0,p.integers[0]))
class TimeOnly:
    descriptor=PolicyDescriptor("sf08.exit.time_only","1.0.0",PolicyKind.EXIT)
    def admissible(self,e,s,f,p):return (PolicyDecision.ADMIT,"") if p.integers[0]>0 else (PolicyDecision.ERROR,"positive horizon required")
    def build(self,e,s,f,p):return ExitPlan(ExitKind.TIME_ONLY,0.0,0.0,False,p.integers[0])
def build_fixture_registry():
    r=PolicyRegistry()
    for p in (ConfirmationMarket(),ReferenceLimit(),AnatomyStop(),BufferedStop(),FixedR(),TimeOnly()):r.register(p)
    r.compile();return r
def params(n0=0.0,i0=0):
    n=[0.0]*8;n[0]=n0;i=[0]*8;i[0]=i0;return PolicyParameters(tuple(n),tuple(i))
def build_reference_matrix(registry):
    m=CandidateMatrixPlan("sf08.reference_matrix","1.0.0")
    m.add(CandidateTemplate("market_invalidation_1r5","1.0.0",True,10,"sf08.entry.confirmation_market","1.0.0",params(2.0,5000),"sf08.stop.anatomy_invalidation","1.0.0",params(),"sf08.exit.fixed_r","1.0.0",params(1.5,3600000),"reference"))
    m.add(CandidateTemplate("reference_buffered_2r","1.0.0",True,20,"sf08.entry.reference_limit","1.0.0",params(0.0,900000),"sf08.stop.buffered_invalidation","1.0.0",params(0.0002,0),"sf08.exit.fixed_r","1.0.0",params(2.0,7200000),"reference"))
    m.compile(registry);return m
