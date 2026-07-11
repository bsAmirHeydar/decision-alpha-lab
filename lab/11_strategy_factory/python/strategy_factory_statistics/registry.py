from __future__ import annotations
from dataclasses import dataclass
from .hashing import stable_id

@dataclass(frozen=True,slots=True)
class MetricDescriptor:
    metric_id:str; version:str; unit:str; aggregation:str; minimum_count:int
    def canonical(self)->str:return f"{self.metric_id}|{self.version}|{self.unit}|{self.aggregation}|{self.minimum_count}"

class MetricRegistry:
    def __init__(self, items:list[MetricDescriptor]):
        ids=[x.metric_id for x in items]
        if len(ids)!=len(set(ids)): raise ValueError("duplicate metric id")
        self.items=tuple(sorted(items,key=lambda x:x.metric_id))
        self.registry_hash=stable_id("mreg",";".join(x.canonical() for x in self.items))

def default_metric_registry()->MetricRegistry:
    return MetricRegistry([
        MetricDescriptor("fill_rate","1.0.0","proportion","wilson",30),
        MetricDescriptor("win_rate","1.0.0","proportion","wilson",30),
        MetricDescriptor("mean_net_r","1.0.0","R","cluster_bootstrap",30),
        MetricDescriptor("median_net_r","1.0.0","R","descriptive",30),
        MetricDescriptor("profit_factor","1.0.0","ratio","descriptive",30),
        MetricDescriptor("maximum_drawdown_r","1.0.0","R","path",30),
        MetricDescriptor("average_mfe_r","1.0.0","R","cluster_bootstrap",30),
        MetricDescriptor("average_mae_r","1.0.0","R","cluster_bootstrap",30),
    ])
