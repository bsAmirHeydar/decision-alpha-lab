from .models import PassSummary,ResearchMetrics
from .enums import PassStatus
FRAME_SIZE=24

def to_frame(s:PassSummary)->list[float]:
    m=s.metrics
    return [float(int(s.status)),m.outcome_count,m.filled_count,m.unique_event_count,m.unique_cluster_count,m.fill_rate,m.win_rate,m.expectancy_r,m.standard_deviation_r,m.profit_factor,m.total_net_r,m.maximum_drawdown_r,m.average_mfe_r,m.average_mae_r,m.average_holding_seconds,m.best_trade_r,m.worst_trade_r,m.best_trade_share,m.maximum_consecutive_losses,m.fold_survival_score,m.cost_survival_score,m.stability_score,s.objective_score,s.public_id]

def from_frame(run_id:str,manifest_hash:str,parameter_hash:str,public_id:int,value:float,data:list[float])->PassSummary:
    if len(data)<FRAME_SIZE: raise ValueError("frame too short")
    m=ResearchMetrics(outcome_count=int(data[1]),filled_count=int(data[2]),unique_event_count=int(data[3]),unique_cluster_count=int(data[4]),fill_rate=data[5],win_rate=data[6],expectancy_r=data[7],standard_deviation_r=data[8],profit_factor=data[9],total_net_r=data[10],maximum_drawdown_r=data[11],average_mfe_r=data[12],average_mae_r=data[13],average_holding_seconds=data[14],best_trade_r=data[15],worst_trade_r=data[16],best_trade_share=data[17],maximum_consecutive_losses=int(data[18]),fold_survival_score=data[19],cost_survival_score=data[20],stability_score=data[21]).with_hash()
    return PassSummary(public_id,run_id,manifest_hash,parameter_hash,value,PassStatus(int(data[0])),m).with_hash()
