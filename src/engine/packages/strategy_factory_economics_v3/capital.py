from __future__ import annotations
from dataclasses import dataclass,field
from decimal import Decimal
from typing import Mapping
from .contracts import AccountEconomicSnapshot,CapitalRequest,CapitalBudget
from .enums import CapitalPolicyKind
from .utils import dec,stable_id,clamp,safe_id
from .errors import EconomicsError
@dataclass(frozen=True,slots=True)
class CapitalPolicyDescriptor:
    policy_id:str; version:str; kind:CapitalPolicyKind; parameters:Mapping[str,Decimal]; priority:int=100; hard_cap:bool=True
    def __post_init__(self): safe_id(self.policy_id,'policy_id'); safe_id(self.version,'version'); object.__setattr__(self,'parameters',{k:dec(v) for k,v in self.parameters.items()})
    @property
    def exact_key(self): return f'{self.policy_id}@{self.version}'
    @property
    def definition_id(self): return stable_id('ucecap',self.to_dict())
    def to_dict(self): return {'policy_id':self.policy_id,'version':self.version,'kind':self.kind.value,'parameters':dict(self.parameters),'priority':self.priority,'hard_cap':self.hard_cap}
class CapitalPolicyRegistry:
    def __init__(self): self._p={}
    def register(self,p):
        if p.exact_key in self._p: raise EconomicsError('duplicate_capital_policy','duplicate policy',{'exact_key':p.exact_key})
        self._p[p.exact_key]=p; return p
    def resolve(self,key):
        if key not in self._p: raise EconomicsError('missing_capital_policy','policy not found',{'exact_key':key})
        return self._p[key]
    def snapshot(self): return tuple(self._p[k] for k in sorted(self._p))
class CapitalBudgetEngine:
    def _value(self,p:CapitalPolicyDescriptor,a:AccountEconomicSnapshot,r:CapitalRequest,current:Decimal):
        x=p.parameters; k=p.kind
        if k is CapitalPolicyKind.FIXED_CASH: return x.get('cash',Decimal('0'))
        if k is CapitalPolicyKind.EQUITY_FRACTION: return a.equity*x.get('fraction',Decimal('0'))
        if k is CapitalPolicyKind.BALANCE_FRACTION: return a.balance*x.get('fraction',Decimal('0'))
        if k is CapitalPolicyKind.RISK_TIER:
            tier=max(Decimal('0'),min(x.get('tier',Decimal('1')),x.get('max_tier',Decimal('1')))); return x.get('base_cash',current)*tier
        if k is CapitalPolicyKind.VOLATILITY_TARGET:
            target=x.get('target_fraction',Decimal('0.01')); observed=max(r.volatility_fraction,x.get('floor_volatility',Decimal('0.0001'))); return current*min(Decimal('1'),target/observed)
        if k is CapitalPolicyKind.DRAWDOWN_SCALED:
            start=x.get('start_fraction',Decimal('0.05')); stop=x.get('stop_fraction',Decimal('0.25')); dd=a.drawdown_fraction
            scale=Decimal('1') if dd<=start else Decimal('0') if dd>=stop else (stop-dd)/(stop-start); return current*scale
        if k is CapitalPolicyKind.CONFIDENCE_SCALED:
            floor=x.get('confidence_floor',Decimal('0.5')); cap=x.get('confidence_cap',Decimal('0.8')); scale=clamp((r.confidence-floor)/max(Decimal('0.000001'),cap-floor),0,1); return current*scale
        if k is CapitalPolicyKind.CAPPED_KELLY:
            pwin=clamp(r.expected_win_probability,0,1); b=max(r.expected_win_loss_ratio,Decimal('0.000001')); kelly=max(Decimal('0'),pwin-(Decimal('1')-pwin)/b); frac=min(kelly*x.get('kelly_fraction',Decimal('0.25')),x.get('max_fraction',Decimal('0.01'))); return a.equity*frac
        if k is CapitalPolicyKind.PORTFOLIO_BUDGET:
            daily=max(Decimal('0'),x.get('daily_loss_cap',Decimal('0'))-a.daily_loss)
            portfolio=max(Decimal('0'),x.get('portfolio_risk_cap',Decimal('0'))-a.open_planned_risk-a.reserved_risk)
            symbol=max(Decimal('0'),x.get('symbol_risk_cap',Decimal('999999999'))-dec(a.symbol_risk.get(r.symbol,0)))
            strategy=max(Decimal('0'),x.get('strategy_risk_cap',Decimal('999999999'))-dec(a.strategy_risk.get(r.strategy_id,0)))
            group=max(Decimal('0'),x.get('group_risk_cap',Decimal('999999999'))-dec(a.group_risk.get(r.correlation_group,0)))
            return min(current,daily,portfolio,symbol,strategy,group)
        return current
    def evaluate(self,policies,account,request):
        ordered=sorted(policies,key=lambda p:(p.priority,p.exact_key)); current=Decimal('Infinity'); requested=Decimal('0'); reductions={}; ids=[]
        for i,p in enumerate(ordered):
            ids.append(p.definition_id); v=max(Decimal('0'),self._value(p,account,request,Decimal('0') if current.is_infinite() else current))
            if i==0: current=requested=v
            elif p.hard_cap:
                if v<current: reductions[p.exact_key]=current-v
                current=min(current,v)
            else: current=v
        if current.is_infinite(): current=Decimal('0')
        return CapitalBudget(request.request_id,tuple(ids),requested,current,reductions,current>0,'ok' if current>0 else 'zero_budget')

def default_capital_registry():
    r=CapitalPolicyRegistry()
    r.register(CapitalPolicyDescriptor('capital.fixed_cash','1.0.0',CapitalPolicyKind.FIXED_CASH,{'cash':Decimal('100')},10))
    r.register(CapitalPolicyDescriptor('capital.equity_fraction','1.0.0',CapitalPolicyKind.EQUITY_FRACTION,{'fraction':Decimal('0.005')},10))
    r.register(CapitalPolicyDescriptor('capital.drawdown_guard','1.0.0',CapitalPolicyKind.DRAWDOWN_SCALED,{'start_fraction':Decimal('0.05'),'stop_fraction':Decimal('0.20')},30))
    r.register(CapitalPolicyDescriptor('capital.confidence_tier','1.0.0',CapitalPolicyKind.CONFIDENCE_SCALED,{'confidence_floor':Decimal('0.50'),'confidence_cap':Decimal('0.80')},40))
    r.register(CapitalPolicyDescriptor('capital.capped_kelly','1.0.0',CapitalPolicyKind.CAPPED_KELLY,{'kelly_fraction':Decimal('0.25'),'max_fraction':Decimal('0.01')},20))
    r.register(CapitalPolicyDescriptor('capital.portfolio_guard','1.0.0',CapitalPolicyKind.PORTFOLIO_BUDGET,{'daily_loss_cap':Decimal('500'),'portfolio_risk_cap':Decimal('1000'),'symbol_risk_cap':Decimal('300'),'strategy_risk_cap':Decimal('500'),'group_risk_cap':Decimal('600')},100))
    return r
