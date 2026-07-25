from __future__ import annotations
import math
from .models import ResearchMetrics,ObjectiveConfig,ObjectiveResult
from .enums import ObjectiveMode,PassStatus

def evaluate_objective(m:ResearchMetrics,c:ObjectiveConfig)->ObjectiveResult:
    if not all(math.isfinite(x) for x in (m.expectancy_r,m.maximum_drawdown_r,m.standard_deviation_r)): return ObjectiveResult(-1e100,PassStatus.REJECTED_NONFINITE,"non-finite metric")
    if m.unique_event_count<c.minimum_unique_events or m.filled_count<c.minimum_filled_outcomes: return ObjectiveResult(-1e100,PassStatus.REJECTED_MIN_SAMPLE,"minimum sample gate failed")
    if m.fill_rate<c.minimum_fill_rate: return ObjectiveResult(-1e100,PassStatus.REJECTED_FILL_RATE,"minimum fill-rate gate failed")
    if m.expectancy_r<c.minimum_expectancy_r: return ObjectiveResult(-1e100,PassStatus.REJECTED_EXPECTANCY,"minimum expectancy gate failed")
    if m.fold_survival_score<c.minimum_fold_survival or m.cost_survival_score<c.minimum_cost_survival or m.stability_score<c.minimum_stability: return ObjectiveResult(-1e100,PassStatus.REJECTED_RECONCILIATION,"survival gate failed")
    survival=m.fold_survival_score*m.cost_survival_score*m.stability_score
    if c.mode==ObjectiveMode.EXPECTANCY: penalty=1.0
    elif c.mode==ObjectiveMode.STABILITY_WEIGHTED: penalty=1+c.drawdown_penalty_weight*m.maximum_drawdown_r
    elif c.mode==ObjectiveMode.TAIL_AWARE: penalty=1+c.drawdown_penalty_weight*m.maximum_drawdown_r+c.tail_dependency_penalty_weight*max(0,m.best_trade_share)
    else: penalty=1+c.drawdown_penalty_weight*m.maximum_drawdown_r+c.dispersion_penalty_weight*m.standard_deviation_r+c.tail_dependency_penalty_weight*max(0,m.best_trade_share)
    return ObjectiveResult(m.expectancy_r*math.sqrt(max(1,m.unique_event_count))*survival/max(1e-12,penalty),PassStatus.VALID,"accepted")
