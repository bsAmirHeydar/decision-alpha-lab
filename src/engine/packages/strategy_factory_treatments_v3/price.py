from __future__ import annotations
from dataclasses import dataclass
from decimal import Decimal, ROUND_FLOOR, ROUND_CEILING, ROUND_HALF_UP
from .enums import TradeSide,PriceRole
from .errors import GeometryError
from .utils import dec,require
@dataclass(frozen=True,slots=True)
class PriceEnvironment:
    bid:Decimal; ask:Decimal; point:Decimal; tick_size:Decimal; digits:int; quote_time_ms:int
    stops_level_points:int=0; freeze_level_points:int=0
    def __post_init__(self):
        for n in ('bid','ask','point','tick_size'):
            object.__setattr__(self,n,dec(getattr(self,n)))
        require(self.bid>0 and self.ask>0,'invalid_quote','bid and ask must be positive')
        require(self.ask>=self.bid,'crossed_quote','ask below bid')
        require(self.point>0 and self.tick_size>0,'invalid_tick','point and tick_size must be positive')
    @property
    def spread(self): return self.ask-self.bid
    def executable_entry(self,side:TradeSide)->Decimal: return self.ask if side is TradeSide.LONG else self.bid
    def executable_exit(self,side:TradeSide)->Decimal: return self.bid if side is TradeSide.LONG else self.ask
    def round_tick(self,price:Decimal,rounding=ROUND_HALF_UP)->Decimal:
        units=(dec(price)/self.tick_size).to_integral_value(rounding=rounding); return units*self.tick_size
    def conservative(self,price:Decimal,side:TradeSide,role:PriceRole)->Decimal:
        # Avoid presenting unattainable improvement: long stop/short target round up; short stop/long target round down.
        if role in (PriceRole.STOP,PriceRole.TRAIL): rounding=ROUND_CEILING if side is TradeSide.LONG else ROUND_FLOOR
        elif role is PriceRole.TARGET: rounding=ROUND_FLOOR if side is TradeSide.LONG else ROUND_CEILING
        else: rounding=ROUND_HALF_UP
        return self.round_tick(dec(price),rounding)
    def points(self,n:Decimal|int|float)->Decimal: return dec(n)*self.point
    def validate_pending(self,side:TradeSide,order_type:str,price:Decimal):
        p=dec(price); min_dist=self.points(self.stops_level_points)
        if order_type=='limit':
            require(p<=self.ask-min_dist if side is TradeSide.LONG else p>=self.bid+min_dist,'pending_distance','limit violates executable-side minimum distance')
        elif order_type=='stop':
            require(p>=self.ask+min_dist if side is TradeSide.LONG else p<=self.bid-min_dist,'pending_distance','stop violates executable-side minimum distance')
    def to_dict(self): return {'bid':self.bid,'ask':self.ask,'point':self.point,'tick_size':self.tick_size,'digits':self.digits,'quote_time_ms':self.quote_time_ms,'stops_level_points':self.stops_level_points,'freeze_level_points':self.freeze_level_points}
