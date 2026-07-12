from __future__ import annotations
from dataclasses import dataclass,field
from decimal import Decimal
from typing import Mapping
from .enums import TradeSide,RuntimeMode
from .price import PriceEnvironment
from .utils import dec,safe_id
@dataclass(frozen=True,slots=True)
class TreatmentBuildContext:
    context_occurrence_id:str; feature_frame_hash:str; side:TradeSide; runtime_mode:RuntimeMode; known_time_ms:int; decision_time_ms:int; price:PriceEnvironment
    reference_price:Decimal|None=None; atr:Decimal|None=None; structural_stop:Decimal|None=None; structural_target:Decimal|None=None
    signal_high:Decimal|None=None; signal_low:Decimal|None=None; context_high:Decimal|None=None; context_low:Decimal|None=None
    swing_high:Decimal|None=None; swing_low:Decimal|None=None; confirmation_price:Decimal|None=None; retest_price:Decimal|None=None
    account_equity:Decimal=Decimal('0'); cash_risk_budget:Decimal=Decimal('0'); portfolio_budget:Decimal=Decimal('0')
    confidence:Decimal=Decimal('0.5'); expected_payoff:Decimal=Decimal('1'); drawdown_fraction:Decimal=Decimal('0'); realized_volatility:Decimal=Decimal('0')
    session_close_ms:int=0; tags:Mapping[str,str]=field(default_factory=dict)
    def __post_init__(self):
        safe_id(self.context_occurrence_id,'context_occurrence_id'); safe_id(self.feature_frame_hash,'feature_frame_hash')
        for n in ('reference_price','atr','structural_stop','structural_target','signal_high','signal_low','context_high','context_low','swing_high','swing_low','confirmation_price','retest_price','account_equity','cash_risk_budget','portfolio_budget','confidence','expected_payoff','drawdown_fraction','realized_volatility'):
            v=getattr(self,n)
            if v is not None: object.__setattr__(self,n,dec(v))
        if self.decision_time_ms<self.known_time_ms: raise ValueError('decision time precedes known time')
    @property
    def available_fields(self): return frozenset(n for n in self.__dataclass_fields__ if getattr(self,n) is not None)
    def level(self,name:str)->Decimal:
        v=getattr(self,name,None)
        if v is None: raise ValueError(f'missing required context level: {name}')
        return dec(v)
