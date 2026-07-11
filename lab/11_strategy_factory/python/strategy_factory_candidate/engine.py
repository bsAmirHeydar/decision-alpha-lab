from __future__ import annotations
from dataclasses import dataclass
from .models import *
from .enums import *
from .hashing import stable_id
@dataclass(slots=True)
class CandidateTelemetry:
    requests:int=0;templates:int=0;disabled:int=0;skips:int=0;errors:int=0;geometry_rejections:int=0;duplicates:int=0;emitted:int=0
class CandidateEngine:
    def __init__(self,registry,matrix,capacity=256):
        if not registry.compiled or not matrix.compiled:raise ValueError("compiled registry and matrix required")
        self.registry=registry;self.matrix=matrix;self.capacity=capacity;self.telemetry=CandidateTelemetry()
    @staticmethod
    def _validate_context(e,s,f):
        if s.event_id!=e.event_id or f.event_id!=e.event_id or f.snapshot_id!=s.snapshot_id:raise ValueError("context identity mismatch")
        if f.state_generation!=s.state_generation:raise ValueError("context generation mismatch")
        if s.snapshot_time_ms<e.known_time_ms:raise ValueError("snapshot precedes known time")
    @staticmethod
    def _validate_geometry(c):
        if c.stop.initial_risk_points<=0:raise ValueError("non-positive risk")
        if c.direction==1:
            if c.stop.stop_price>=c.entry.requested_price:raise ValueError("long stop invalid")
            if c.exit_plan.has_price_target and c.exit_plan.target_price<=c.entry.requested_price:raise ValueError("long target invalid")
        elif c.direction==2:
            if c.stop.stop_price<=c.entry.requested_price:raise ValueError("short stop invalid")
            if c.exit_plan.has_price_target and c.exit_plan.target_price>=c.entry.requested_price:raise ValueError("short target invalid")
        else:raise ValueError("direction invalid")
    def build(self,event,snapshot,frame,generation):
        self.telemetry.requests+=1;self._validate_context(event,snapshot,frame);out=[];seen=set()
        for t in self.matrix.templates:
            self.telemetry.templates+=1
            if not t.enabled:self.telemetry.disabled+=1;continue
            policies=[self.registry.resolve(t.entry_policy_id,t.entry_policy_version),self.registry.resolve(t.stop_policy_id,t.stop_policy_version),self.registry.resolve(t.exit_policy_id,t.exit_policy_version)]
            params=[t.entry_parameters,t.stop_parameters,t.exit_parameters]
            decisions=[p.admissible(event,snapshot,frame,pa) for p,pa in zip(policies,params)]
            if any(d==PolicyDecision.ERROR for d,_ in decisions):self.telemetry.errors+=1;raise ValueError(next(r for d,r in decisions if d==PolicyDecision.ERROR))
            if any(d==PolicyDecision.SKIP for d,_ in decisions):self.telemetry.skips+=1;continue
            entry=policies[0].build(event,snapshot,frame,params[0]);stop=policies[1].build(event,snapshot,frame,params[1]);exit_plan=policies[2].build(event,snapshot,frame,params[2])
            c=TradeCandidate(t.template_id,t.hash,event.event_id,snapshot.snapshot_id,frame.frame_id,event.strategy_id,event.strategy_version,event.symbol,event.direction,generation,snapshot.snapshot_time_ms,entry,stop,exit_plan,stable_id("csrc",event.source_hash+"|"+frame.frame_id+"|"+t.hash))
            try:self._validate_geometry(c)
            except ValueError:self.telemetry.geometry_rejections+=1;continue
            if c.candidate_id in seen:self.telemetry.duplicates+=1;continue
            if len(out)>=self.capacity:raise OverflowError("candidate capacity exceeded")
            seen.add(c.candidate_id);out.append(c);self.telemetry.emitted+=1
        return out
