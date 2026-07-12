from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal,ROUND_CEILING,ROUND_FLOOR,ROUND_HALF_UP
from strategy_factory_treatments_v3.enums import TradeSide
from .contracts import SymbolEconomicsSpec,QuoteSnapshot,RiskGeometry
from .enums import *
from .errors import BrokerConstraintError,StaleEconomicInput
from .utils import dec,floor_step,round_tick
@dataclass(frozen=True,slots=True)
class ConstraintFinding:
    code:str; decision:ConstraintDecision; original:Decimal|str; adjusted:Decimal|str; message:str
    def to_dict(self): return {'code':self.code,'decision':self.decision.value,'original':self.original,'adjusted':self.adjusted,'message':self.message}
@dataclass(frozen=True,slots=True)
class ConstraintResult:
    accepted:bool; entry_price:Decimal; stop_price:Decimal; target_price:Decimal|None; volume:Decimal; margin_required:Decimal; findings:tuple[ConstraintFinding,...]; reason_code:str='ok'
    def to_dict(self): return {'accepted':self.accepted,'entry_price':self.entry_price,'stop_price':self.stop_price,'target_price':self.target_price,'volume':self.volume,'margin_required':self.margin_required,'findings':[x.to_dict() for x in self.findings],'reason_code':self.reason_code}
class BrokerConstraintSolver:
    def validate_freshness(self,spec,decision_time_ms,max_spec_age_ms):
        if spec.age_ms(decision_time_ms)>max_spec_age_ms: raise StaleEconomicInput('stale_spec','symbol specification too old',{'age_ms':spec.age_ms(decision_time_ms)})
    def normalize_price(self,price,spec,rounding=ROUND_HALF_UP): return round_tick(price,spec.tick_size,rounding)
    def margin(self,spec,volume,entry_price,conversion_rate=Decimal('1')):
        volume,entry_price,conversion_rate=map(dec,(volume,entry_price,conversion_rate))
        if spec.margin_mode is MarginMode.FIXED_PER_LOT: return spec.margin_per_lot*volume*conversion_rate
        notional=entry_price*spec.contract_size*volume*conversion_rate
        if spec.margin_mode is MarginMode.NOTIONAL_RATE: return notional*spec.margin_rate
        return notional/spec.leverage
    def solve(self,spec:SymbolEconomicsSpec,quote:QuoteSnapshot,geometry:RiskGeometry,entry_price,stop_price,target_price,raw_volume,free_margin,conversion_rate=Decimal('1'),max_spec_age_ms=86400000):
        self.validate_freshness(spec,geometry and quote.known_time_ms if False else max(quote.known_time_ms,spec.known_time_ms),max_spec_age_ms)
        findings=[]
        if spec.trade_status is not TradeStatus.ENABLED: return ConstraintResult(False,dec(entry_price),dec(stop_price),None if target_price is None else dec(target_price),Decimal('0'),Decimal('0'),(),f'trade_status_{spec.trade_status.value}')
        if geometry.order_kind not in spec.allowed_order_kinds: return ConstraintResult(False,dec(entry_price),dec(stop_price),None if target_price is None else dec(target_price),Decimal('0'),Decimal('0'),(),'order_kind_not_allowed')
        e=self.normalize_price(entry_price,spec,ROUND_CEILING if geometry.side is TradeSide.LONG else ROUND_FLOOR)
        s=self.normalize_price(stop_price,spec,ROUND_FLOOR if geometry.side is TradeSide.LONG else ROUND_CEILING)
        t=None if target_price is None else self.normalize_price(target_price,spec,ROUND_FLOOR if geometry.side is TradeSide.LONG else ROUND_CEILING)
        min_stop=spec.stops_level_points*spec.point
        distance=abs(e-s)
        if distance<min_stop:
            ns=e-min_stop if geometry.side is TradeSide.LONG else e+min_stop
            ns=self.normalize_price(ns,spec,ROUND_FLOOR if geometry.side is TradeSide.LONG else ROUND_CEILING)
            findings.append(ConstraintFinding('minimum_stop_distance',ConstraintDecision.ADJUST,s,ns,'protective stop widened to broker minimum')); s=ns
        v=floor_step(raw_volume,spec.volume_step); v=min(v,spec.volume_max)
        if v!=dec(raw_volume): findings.append(ConstraintFinding('volume_step',ConstraintDecision.ADJUST,dec(raw_volume),v,'volume floored to broker step and maximum'))
        if v<spec.volume_min: return ConstraintResult(False,e,s,t,Decimal('0'),Decimal('0'),tuple(findings),'volume_below_minimum')
        margin=self.margin(spec,v,e,conversion_rate)
        if margin>dec(free_margin):
            per_lot=self.margin(spec,Decimal('1'),e,conversion_rate)
            mv=floor_step(dec(free_margin)/per_lot,spec.volume_step) if per_lot>0 else Decimal('0'); mv=min(mv,spec.volume_max)
            findings.append(ConstraintFinding('margin_cap',ConstraintDecision.ADJUST,v,mv,'volume reduced by free margin')); v=mv; margin=self.margin(spec,v,e,conversion_rate)
        if v<spec.volume_min: return ConstraintResult(False,e,s,t,Decimal('0'),margin,tuple(findings),'insufficient_margin')
        return ConstraintResult(True,e,s,t,v,margin,tuple(findings),'ok')
