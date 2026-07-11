from __future__ import annotations
from .models import PathEvent,PriceObservation
from .enums import PathEventKind
from .hashing import stable_id,cdouble
class PathTracker:
    def __init__(self,direction:int,entry_price:float,risk_points:float,capacity:int=64):
        if direction not in (1,2) or entry_price<=0 or risk_points<=0 or not 0<capacity<=96:raise ValueError("invalid path tracker")
        self.direction=direction;self.entry_price=entry_price;self.risk_points=risk_points;self.capacity=capacity;self.events=[];self.mfe_points=0.0;self.mae_points=0.0;self.path_hash="path_empty"
    def append(self,kind,time_ms,price,fav=0.0,adv=0.0):
        if len(self.events)>=self.capacity:raise OverflowError("path capacity")
        seq=len(self.events);h=stable_id("pevt",f"{self.path_hash}|{seq}|{int(kind)}|{time_ms}|{cdouble(price)}|{cdouble(fav)}|{cdouble(adv)}")
        self.events.append(PathEvent(seq,kind,time_ms,price,fav,adv,h));self.path_hash=h
    def update(self,o:PriceObservation):
        if self.direction==1:fav=max(0,o.high-self.entry_price);adv=max(0,self.entry_price-o.low)
        else:fav=max(0,self.entry_price-o.low);adv=max(0,o.high-self.entry_price)
        if fav>self.mfe_points:self.mfe_points=fav;self.append(PathEventKind.FAVORABLE_EXTREME,o.observed_at_ms,o.close,fav,adv)
        if adv>self.mae_points:self.mae_points=adv;self.append(PathEventKind.ADVERSE_EXTREME,o.observed_at_ms,o.close,fav,adv)
    @property
    def mfe_r(self):return self.mfe_points/self.risk_points
    @property
    def mae_r(self):return self.mae_points/self.risk_points
