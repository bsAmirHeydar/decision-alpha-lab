from __future__ import annotations
from dataclasses import dataclass,field
from .enums import *
from .hashing import stable_id,cdouble

@dataclass(frozen=True,slots=True)
class PriceObservation:
    symbol:str; kind:ObservationKind; fidelity:DataFidelity; sequence:int; observed_at_ms:int; interval_open_ms:int; interval_close_ms:int
    open:float; high:float; low:float; close:float; spread_points:float=0.0; bid:float|None=None; ask:float|None=None; source_hash:str="src"
    def __post_init__(self):
        if not self.symbol or self.sequence<0: raise ValueError("invalid observation identity")
        if self.interval_close_ms<self.interval_open_ms or self.observed_at_ms<self.interval_close_ms: raise ValueError("invalid observation time")
        if self.low<=0 or self.high<self.low or not(self.low<=self.open<=self.high) or not(self.low<=self.close<=self.high): raise ValueError("invalid OHLC")
        if (self.bid is None)!=(self.ask is None): raise ValueError("bid and ask must be paired")
        if self.bid is not None and self.ask<self.bid: raise ValueError("ask below bid")
        if self.spread_points<0: raise ValueError("negative spread")
    @property
    def canonical(self)->str:
        return "|".join(map(str,[self.symbol,int(self.kind),int(self.fidelity),self.sequence,self.observed_at_ms,self.interval_open_ms,self.interval_close_ms,cdouble(self.open),cdouble(self.high),cdouble(self.low),cdouble(self.close),str(self.bid is not None).lower(),cdouble(self.bid or 0),cdouble(self.ask or 0),cdouble(self.spread_points),self.source_hash]))
    @property
    def observation_id(self)->str:return stable_id("pobs",self.canonical)

@dataclass(frozen=True,slots=True)
class SimulationPolicy:
    policy_id:str="sf09.conservative"; version:str="1.0.0"; ambiguity:AmbiguityPolicy=AmbiguityPolicy.STOP_FIRST
    gap:GapPolicy=GapPolicy.AT_OBSERVED_OPEN_CONSERVATIVE; market_fill:MarketFillPolicy=MarketFillPolicy.CONSERVATIVE_SIDE
    minimum_fidelity:DataFidelity=DataFidelity.BAR_APPROXIMATION; allow_limit_improvement:bool=False; allow_stop_gap_slippage:bool=True
    strict_monotonic:bool=True; fail_on_stale:bool=True; max_observation_age_ms:int=300_000; max_path_events:int=64
    def __post_init__(self):
        if self.max_observation_age_ms<0 or not 0<self.max_path_events<=96: raise ValueError("invalid simulation bounds")
    @property
    def canonical(self):return "|".join(map(str,[self.policy_id,self.version,int(self.ambiguity),int(self.gap),int(self.market_fill),int(self.minimum_fidelity),str(self.allow_limit_improvement).lower(),str(self.allow_stop_gap_slippage).lower(),str(self.strict_monotonic).lower(),str(self.fail_on_stale).lower(),self.max_observation_age_ms,self.max_path_events]))
    @property
    def policy_hash(self):return stable_id("spol",self.canonical)

@dataclass(frozen=True,slots=True)
class CostBreakdown:
    model_id:str; model_version:str; entry_spread_points:float; exit_spread_points:float; entry_slippage_points:float; exit_slippage_points:float; commission_r:float; other_r:float; total_cost_points:float; total_cost_r:float
    @property
    def canonical(self):return "|".join(map(str,[self.model_id,self.model_version,*map(cdouble,[self.entry_spread_points,self.exit_spread_points,self.entry_slippage_points,self.exit_slippage_points,self.commission_r,self.other_r,self.total_cost_points,self.total_cost_r])]))
    @property
    def cost_hash(self):return stable_id("cost",self.canonical)

@dataclass(frozen=True,slots=True)
class PathEvent:
    sequence:int; kind:PathEventKind; time_ms:int; price:float; favorable_points:float; adverse_points:float; event_hash:str

@dataclass(frozen=True,slots=True)
class OutcomeRecord:
    candidate_id:str; event_id:str; strategy_id:str; symbol:str; direction:int; terminal_state:RuntimeState; exit_reason:ExitReason; fidelity:DataFidelity
    filled:bool; ambiguous:bool; partial_exit_used:bool; registered_at_ms:int; fill_time_ms:int; fill_price:float; exit_time_ms:int; exit_price:float
    gross_points:float; gross_r:float; net_r:float; mfe_points:float; mae_points:float; mfe_r:float; mae_r:float; holding_ms:int; time_to_fill_ms:int
    costs:CostBreakdown; simulation_policy_hash:str; cost_registry_hash:str; path_hash:str; source_hash:str; remaining_fraction:float=0.0
    @property
    def canonical(self):
        return "|".join(map(str,["alpha_lab.strategy_factory/outcome_record@1.0.0",self.candidate_id,self.event_id,self.strategy_id,self.symbol,self.direction,int(self.terminal_state),int(self.exit_reason),int(self.fidelity),str(self.filled).lower(),str(self.ambiguous).lower(),str(self.partial_exit_used).lower(),self.registered_at_ms,self.fill_time_ms,cdouble(self.fill_price),self.exit_time_ms,cdouble(self.exit_price),cdouble(self.remaining_fraction),cdouble(self.gross_points),cdouble(self.gross_r),cdouble(self.net_r),cdouble(self.mfe_points),cdouble(self.mae_points),cdouble(self.mfe_r),cdouble(self.mae_r),self.holding_ms,self.time_to_fill_ms,self.costs.cost_hash,self.simulation_policy_hash,self.cost_registry_hash,self.path_hash,self.source_hash]))
    @property
    def outcome_id(self):return stable_id("outc",self.canonical)
    def validate(self):
        if self.terminal_state not in {RuntimeState.CLOSED,RuntimeState.EXPIRED,RuntimeState.INVALIDATED,RuntimeState.AMBIGUOUS,RuntimeState.REJECTED}: raise ValueError("non-terminal outcome")
        if abs(self.net_r-(self.gross_r-self.costs.total_cost_r))>1e-9: raise ValueError("net R mismatch")
        if self.mfe_r<0 or self.mae_r<0 or not 0<=self.remaining_fraction<=1: raise ValueError("invalid outcome bounds")
        return self
