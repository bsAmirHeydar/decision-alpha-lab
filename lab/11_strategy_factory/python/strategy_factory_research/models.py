from __future__ import annotations
from dataclasses import dataclass, field, asdict
from .enums import *
from .hashing import stable_id
import math

@dataclass(frozen=True, slots=True)
class OutcomeView:
    outcome_id:str; candidate_id:str; event_id:str; cluster_id:str; filled:bool; ambiguous:bool; net_r:float; mfe_r:float; mae_r:float; holding_seconds:float
    def validate(self)->None:
        if not self.outcome_id or not self.event_id: raise ValueError("missing outcome identity")
        for v in (self.net_r,self.mfe_r,self.mae_r,self.holding_seconds):
            if not math.isfinite(v): raise ValueError("non-finite outcome")
        if self.mfe_r<0 or self.mae_r<0 or self.holding_seconds<0: raise ValueError("invalid outcome bounds")

@dataclass(frozen=True, slots=True)
class ResearchMetrics:
    outcome_count:int=0; filled_count:int=0; win_count:int=0; loss_count:int=0; flat_count:int=0; ambiguous_count:int=0; no_fill_count:int=0
    unique_event_count:int=0; unique_cluster_count:int=0; fill_rate:float=0.0; win_rate:float=0.0; average_win_r:float=0.0; average_loss_r:float=0.0
    expectancy_r:float=0.0; standard_deviation_r:float=0.0; profit_factor:float=0.0; total_net_r:float=0.0; maximum_drawdown_r:float=0.0
    maximum_runup_r:float=0.0; average_mfe_r:float=0.0; average_mae_r:float=0.0; average_holding_seconds:float=0.0; best_trade_r:float=0.0
    worst_trade_r:float=0.0; best_trade_share:float=0.0; maximum_consecutive_losses:int=0; fold_survival_score:float=1.0; cost_survival_score:float=1.0; stability_score:float=1.0
    metrics_hash:str=""
    def canonical(self)->str:
        vals=[self.outcome_count,self.filled_count,self.unique_event_count,self.unique_cluster_count,self.fill_rate,self.win_rate,self.expectancy_r,self.standard_deviation_r,self.profit_factor,self.total_net_r,self.maximum_drawdown_r,self.best_trade_share,self.fold_survival_score,self.cost_survival_score,self.stability_score]
        return "alpha_lab.strategy_factory/research_metrics@1.0.0|"+"|".join(str(v) for v in vals)
    def with_hash(self):
        return type(self)(**{**asdict(self),"metrics_hash":stable_id("rmet",self.canonical())})

@dataclass(frozen=True, slots=True)
class ObjectiveConfig:
    mode:ObjectiveMode=ObjectiveMode.CONSERVATIVE; minimum_unique_events:int=30; minimum_filled_outcomes:int=20; minimum_fill_rate:float=.1; minimum_expectancy_r:float=0.0
    drawdown_penalty_weight:float=1.0; dispersion_penalty_weight:float=.25; tail_dependency_penalty_weight:float=1.0; minimum_fold_survival:float=0.0; minimum_cost_survival:float=0.0; minimum_stability:float=0.0

@dataclass(frozen=True, slots=True)
class ObjectiveResult: score:float; status:PassStatus; reason:str

@dataclass(frozen=True, slots=True)
class RunManifest:
    run_id:str; research_program_id:str; strategy_id:str; strategy_version:str; runtime_generation_id:int; runtime_generation_hash:str; plugin_set_hash:str
    candidate_matrix_hash:str; simulation_policy_hash:str; cost_registry_hash:str; input_parameter_hash:str; data_source_id:str; symbol:str; timeframe_seconds:int
    test_start_utc_msc:int; test_end_utc_msc:int; fidelity_preset:FidelityPresetKind; objective_mode:ObjectiveMode; export_detail:int; random_seed:int; git_commit:str; terminal_build:str; source_hash:str; manifest_hash:str=""
    schema:str="alpha_lab.strategy_factory/research_run_manifest@1.0.0"
    def canonical(self)->str:
        fields=[self.schema,self.run_id,self.research_program_id,self.strategy_id,self.strategy_version,self.runtime_generation_id,self.runtime_generation_hash,self.plugin_set_hash,self.candidate_matrix_hash,self.simulation_policy_hash,self.cost_registry_hash,self.input_parameter_hash,self.data_source_id,self.symbol,self.timeframe_seconds,self.test_start_utc_msc,self.test_end_utc_msc,int(self.fidelity_preset),int(self.objective_mode),self.export_detail,self.random_seed,self.git_commit,self.terminal_build,self.source_hash]
        return "|".join(map(str,fields))
    def derived_hash(self)->str: return stable_id("rman",self.canonical())
    def validate(self)->None:
        if self.test_end_utc_msc<=self.test_start_utc_msc or self.timeframe_seconds<=0: raise ValueError("invalid run range")
        if self.manifest_hash and self.manifest_hash!=self.derived_hash(): raise ValueError("manifest hash mismatch")

@dataclass(frozen=True, slots=True)
class PassSummary:
    public_id:int; run_id:str; manifest_hash:str; parameter_hash:str; objective_score:float; status:PassStatus; metrics:ResearchMetrics; summary_hash:str=""
    schema:str="alpha_lab.strategy_factory/optimization_pass_summary@1.0.0"
    def canonical(self)->str: return f"{self.schema}|{self.public_id}|{self.run_id}|{self.manifest_hash}|{self.parameter_hash}|{self.objective_score}|{int(self.status)}|{self.metrics.metrics_hash}"
    def with_hash(self): return type(self)(**{**asdict(self),"status":self.status,"metrics":self.metrics,"summary_hash":stable_id("psum",self.canonical())})

@dataclass(frozen=True, slots=True)
class FidelityPreset:
    preset_id:str; preset_version:str; preset:FidelityPresetKind; minimum_observation_fidelity:int; require_spread:bool; require_bid_ask:bool; reject_ambiguous_bars:bool; require_differential_validation:bool; maximum_selected_passes:int
