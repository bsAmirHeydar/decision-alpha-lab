from __future__ import annotations
from dataclasses import dataclass
from strategy_factory_candidate import TradeCandidate,OrderKind
from .enums import *
from .models import *
from .costs import CostRegistry,CostRequest
from .path import PathTracker

@dataclass
class Runtime:
    candidate:TradeCandidate; registered_at_ms:int; state:RuntimeState=RuntimeState.REGISTERED; last_sequence:int=-1; filled:bool=False; fill_time_ms:int=0; fill_price:float=0.0; entry_spread:float=0.0; remaining:float=1.0; realized_weighted_points:float=0.0; target_consumed:bool=False; ambiguous:bool=False; fidelity:DataFidelity=DataFidelity.UNKNOWN; path:PathTracker|None=None

class OutcomeEngine:
    def __init__(self,policy:SimulationPolicy,cost_registry:CostRegistry,cost_model_id:str,cost_model_version:str,capacity=256):
        if not 0<capacity<=256:raise ValueError("capacity")
        self.policy=policy;self.cost_registry=cost_registry;self.cost_model_id=cost_model_id;self.cost_model_version=cost_model_version;self.capacity=capacity;self.active=[];self.outcomes=[];self.telemetry={k:0 for k in ["registered","observations","duplicates","out_of_order","fills","targets","stops","time_exits","expirations","ambiguities","partials","terminal"]}
    def register(self,c:TradeCandidate,registered_at_ms:int):
        if len(self.active)>=self.capacity:raise OverflowError("active capacity")
        if any(r.candidate.candidate_id==c.candidate_id and r.state not in {RuntimeState.CLOSED,RuntimeState.EXPIRED,RuntimeState.INVALIDATED,RuntimeState.AMBIGUOUS,RuntimeState.REJECTED} for r in self.active):raise ValueError("duplicate active candidate")
        p=PathTracker(c.direction,c.entry.requested_price,c.stop.initial_risk_points,self.policy.max_path_events);p.append(PathEventKind.REGISTERED,registered_at_ms,c.entry.requested_price)
        self.active.append(Runtime(c,registered_at_ms,path=p));self.telemetry["registered"]+=1
    def _current(self,o,direction,entry):
        if o.bid is not None:return o.ask if entry and direction==1 else o.bid if entry else o.bid if direction==1 else o.ask
        return o.open
    def _entry(self,c,o):
        p=c.entry.requested_price
        if c.entry.order_kind==OrderKind.MARKET:return self._current(o,c.direction,True)
        if c.entry.order_kind==OrderKind.LIMIT:
            touched=o.low<=p if c.direction==1 else o.high>=p
            if not touched:return None
            return min(p,o.open) if self.policy.allow_limit_improvement and c.direction==1 else max(p,o.open) if self.policy.allow_limit_improvement else p
        if c.entry.order_kind==OrderKind.STOP:
            touched=o.high>=p if c.direction==1 else o.low<=p
            if not touched:return None
            return max(p,o.open) if self.policy.allow_stop_gap_slippage and c.direction==1 else min(p,o.open) if self.policy.allow_stop_gap_slippage else p
        return None
    def _signed(self,r,px):return px-r.fill_price if r.candidate.direction==1 else r.fill_price-px
    def _finalize(self,r,state,reason,time_ms,price,exit_spread):
        pts=r.realized_weighted_points+(r.remaining*self._signed(r,price) if r.filled else 0.0);gross=pts/r.candidate.stop.initial_risk_points if r.filled else 0.0
        if r.filled:cost=self.cost_registry.resolve(self.cost_model_id,self.cost_model_version).compute(CostRequest(r.candidate.candidate_id,r.candidate.stop.initial_risk_points,r.entry_spread,exit_spread))
        else:cost=self.cost_registry.resolve(self.cost_model_id,self.cost_model_version).compute(CostRequest(r.candidate.candidate_id,r.candidate.stop.initial_risk_points,0,0));cost=CostBreakdown(cost.model_id,cost.model_version,0,0,0,0,0,0,0,0)
        out=OutcomeRecord(r.candidate.candidate_id,r.candidate.event_id,r.candidate.strategy_id,r.candidate.symbol,r.candidate.direction,state,reason,r.fidelity,r.filled,r.ambiguous,r.remaining<1,r.registered_at_ms,r.fill_time_ms,r.fill_price,time_ms,price,pts,gross,gross-cost.total_cost_r,r.path.mfe_points,r.path.mae_points,r.path.mfe_r,r.path.mae_r,time_ms-r.fill_time_ms if r.filled else 0,r.fill_time_ms-r.registered_at_ms if r.filled else 0,cost,self.policy.policy_hash,self.cost_registry.registry_hash,r.path.path_hash,r.candidate.source_hash).validate()
        r.state=state;self.outcomes.append(out);self.telemetry["terminal"]+=1
    def process(self,o:PriceObservation):
        self.telemetry["observations"]+=1
        for r in self.active:
            if r.state in {RuntimeState.CLOSED,RuntimeState.EXPIRED,RuntimeState.INVALIDATED,RuntimeState.AMBIGUOUS,RuntimeState.REJECTED} or r.candidate.symbol!=o.symbol:continue
            if o.sequence==r.last_sequence:self.telemetry["duplicates"]+=1;continue
            if self.policy.strict_monotonic and r.last_sequence>=0 and o.sequence<r.last_sequence:self.telemetry["out_of_order"]+=1;raise ValueError("out of order")
            r.last_sequence=o.sequence;r.fidelity=o.fidelity;now=o.observed_at_ms
            if not r.filled:
                if now<r.candidate.entry.activation_time_ms:r.state=RuntimeState.WAITING_ACTIVATION;continue
                if now>r.candidate.entry.expiration_time_ms:self._finalize(r,RuntimeState.EXPIRED,ExitReason.ENTRY_EXPIRED,now,o.close,0);self.telemetry["expirations"]+=1;continue
                r.state=RuntimeState.PENDING_FILL;px=self._entry(r.candidate,o)
                if px is None:continue
                r.filled=True;r.state=RuntimeState.FILLED;r.fill_time_ms=now;r.fill_price=px;r.entry_spread=o.spread_points;r.path=PathTracker(r.candidate.direction,px,r.candidate.stop.initial_risk_points,self.policy.max_path_events);r.path.append(PathEventKind.FILLED,now,px);self.telemetry["fills"]+=1
            r.path.update(o)
            stop=o.low<=r.candidate.stop.stop_price if r.candidate.direction==1 else o.high>=r.candidate.stop.stop_price
            target=(not r.target_consumed) and r.candidate.exit_plan.has_price_target and (o.high>=r.candidate.exit_plan.target_price if r.candidate.direction==1 else o.low<=r.candidate.exit_plan.target_price)
            if stop and target:
                r.ambiguous=True;self.telemetry["ambiguities"]+=1
                if self.policy.ambiguity in {AmbiguityPolicy.EXCLUDE,AmbiguityPolicy.REQUIRE_LOWER_FIDELITY}:
                    self._finalize(r,RuntimeState.AMBIGUOUS,ExitReason.AMBIGUOUS_BAR,now,o.close,o.spread_points);continue
            resolve_stop=stop and (not target or self.policy.ambiguity==AmbiguityPolicy.STOP_FIRST)
            resolve_target=target and (not stop or self.policy.ambiguity==AmbiguityPolicy.TARGET_FIRST)
            if resolve_stop:
                reason=ExitReason.PARTIAL_TARGET_THEN_STOP if r.remaining<1 else ExitReason.STOP
                self._finalize(r,RuntimeState.CLOSED,reason,now,r.candidate.stop.stop_price,o.spread_points);self.telemetry["stops"]+=1;continue
            if resolve_target:
                pf=r.candidate.exit_plan.partial_fraction
                if 0<pf<1:
                    r.realized_weighted_points+=pf*self._signed(r,r.candidate.exit_plan.target_price);r.remaining-=pf;r.target_consumed=True;r.state=RuntimeState.PARTIAL;self.telemetry["partials"]+=1;continue
                self._finalize(r,RuntimeState.CLOSED,ExitReason.TARGET,now,r.candidate.exit_plan.target_price,o.spread_points);self.telemetry["targets"]+=1;continue
            held=now-r.fill_time_ms
            if r.candidate.exit_plan.max_holding_ms>0 and held>=r.candidate.exit_plan.max_holding_ms:
                reason=ExitReason.PARTIAL_TARGET_THEN_TIME if r.remaining<1 else ExitReason.TIME
                self._finalize(r,RuntimeState.CLOSED,reason,now,self._current(o,r.candidate.direction,False),o.spread_points);self.telemetry["time_exits"]+=1
    def pop(self):return self.outcomes.pop(0) if self.outcomes else None
