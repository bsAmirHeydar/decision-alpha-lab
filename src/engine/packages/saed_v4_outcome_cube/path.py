from __future__ import annotations
from .canonical import content_hash
from .models import PathEvent
from .errors import BudgetError
class PathLedger:
    def __init__(self,direction:int,entry_price:float,risk_points:float,capacity:int):
        self.direction=direction;self.entry_price=entry_price;self.risk_points=risk_points;self.capacity=capacity;self.events=[];self.mfe=0.0;self.mae=0.0
    def append(self,kind,time_ms,price,remaining=1.0):
        if len(self.events)>=self.capacity:raise BudgetError('maximum path events exceeded')
        fav=max(0.0,(price-self.entry_price)*self.direction);adv=max(0.0,(self.entry_price-price)*self.direction)
        seed={'previous_hash':self.events[-1].event_hash if self.events else 'GENESIS','sequence':len(self.events),'kind':kind,'time_ms':time_ms,'price':price,'favorable_points':fav,'adverse_points':adv,'remaining_fraction':remaining}
        self.events.append(PathEvent(len(self.events),kind,time_ms,price,fav,adv,remaining,content_hash(seed)))
    def update_extremes(self,o,remaining=1.0):
        favorable=max(0.0,(o.high-self.entry_price) if self.direction==1 else (self.entry_price-o.low)); adverse=max(0.0,(self.entry_price-o.low) if self.direction==1 else (o.high-self.entry_price))
        if favorable>self.mfe:self.mfe=favorable;self.append('favorable_extreme',o.observed_at_ms,o.high if self.direction==1 else o.low,remaining)
        if adverse>self.mae:self.mae=adverse;self.append('adverse_extreme',o.observed_at_ms,o.low if self.direction==1 else o.high,remaining)
