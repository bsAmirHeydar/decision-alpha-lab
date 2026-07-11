from __future__ import annotations
from collections import defaultdict
from statistics import median
import math
from .models import StatisticalSample, StatisticSummary
from .enums import ReportStatus
from .streaming import DistributionAccumulator

_ALLOWED = {
    "all", "strategy_id", "symbol", "direction", "session_id", "year",
    "month", "weekday", "stratum_key", "filled", "ambiguous"
}

def group_key(sample: StatisticalSample, dimensions: tuple[str, ...]) -> str:
    if not dimensions or dimensions == ("all",): return "all=all"
    parts=[]
    for name in dimensions:
        if name not in _ALLOWED or name == "all": raise ValueError(f"unsupported group dimension: {name}")
        parts.append(f"{name}={getattr(sample, name)}")
    return "|".join(parts)

class GroupedStatisticsEngine:
    def __init__(self, minimum_sample_count: int = 1, quantile_capacity: int = 4096) -> None:
        self.minimum_sample_count=minimum_sample_count; self.quantile_capacity=quantile_capacity
    def summarize(self, samples: list[StatisticalSample], dimensions: tuple[str,...] = ("all",)) -> list[StatisticSummary]:
        groups: dict[str,list[StatisticalSample]]=defaultdict(list)
        for s in samples: s.validate(); groups[group_key(s,dimensions)].append(s)
        return [self._one(k,groups[k]) for k in sorted(groups)]
    def _one(self,key: str, rows: list[StatisticalSample]) -> StatisticSummary:
        filled=[r for r in rows if r.filled]
        acc=DistributionAccumulator(self.quantile_capacity)
        for r in filled: acc.add(r.net_r)
        wins=[r.net_r for r in filled if r.net_r>0]; losses=[r.net_r for r in filled if r.net_r<0]
        total=sum(r.net_r for r in filled); best=max((r.net_r for r in filled),default=0.0)
        n=len(filled); status=ReportStatus.VALID if len(rows)>=self.minimum_sample_count else ReportStatus.INSUFFICIENT_SAMPLE
        summary=StatisticSummary(
            group_key=key, sample_count=len(rows), filled_count=n, win_count=len(wins), loss_count=len(losses),
            flat_count=n-len(wins)-len(losses), unique_event_count=len({r.event_id for r in rows}),
            unique_cluster_count=len({r.cluster_id for r in rows}), fill_rate=n/len(rows) if rows else 0.0,
            win_rate=len(wins)/n if n else 0.0, mean_net_r=acc.moments.mean if n else 0.0,
            median_net_r=median([r.net_r for r in filled]) if n else 0.0,
            standard_deviation_r=acc.moments.standard_deviation if n else 0.0,
            standard_error_r=acc.moments.standard_error if n else 0.0,
            profit_factor=acc.profit_factor if n else 0.0, total_net_r=total,
            maximum_drawdown_r=acc.drawdown.maximum_drawdown,
            average_mfe_r=sum(r.mfe_r for r in filled)/n if n else 0.0,
            average_mae_r=sum(r.mae_r for r in filled)/n if n else 0.0,
            average_holding_seconds=sum(r.holding_seconds for r in filled)/n if n else 0.0,
            q05_net_r=acc.quantiles.quantile(.05), q25_net_r=acc.quantiles.quantile(.25),
            q75_net_r=acc.quantiles.quantile(.75), q95_net_r=acc.quantiles.quantile(.95),
            best_trade_r=best, worst_trade_r=min((r.net_r for r in filled),default=0.0),
            best_trade_share=best/total if best>0 and total>0 else 0.0, status=status)
        return summary.with_hash()
