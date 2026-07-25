from __future__ import annotations
from math import sqrt
from statistics import stdev
from .models import OutcomeView, ResearchMetrics

class ResearchAccumulator:
    def __init__(self,max_unique:int=100000):
        self.max_unique=max_unique; self.outcomes=[]; self.events=set(); self.clusters=set()
    def observe(self,o:OutcomeView)->None:
        o.validate(); self.events.add(o.event_id); self.clusters.add(o.cluster_id or o.event_id)
        if len(self.events)>self.max_unique or len(self.clusters)>self.max_unique: raise OverflowError("unique-key capacity exceeded")
        self.outcomes.append(o)
    def snapshot(self,fold_survival:float=1.0,cost_survival:float=1.0,stability:float=1.0)->ResearchMetrics:
        filled=[o for o in self.outcomes if o.filled]; rs=[o.net_r for o in filled]; wins=[r for r in rs if r>0]; losses=[r for r in rs if r<0]
        equity=peak=trough=max_dd=max_ru=0.0; streak=max_streak=0
        for r in rs:
            equity+=r; peak=max(peak,equity); max_dd=max(max_dd,peak-equity); trough=min(trough,equity); max_ru=max(max_ru,equity-trough)
            if r<0: streak+=1; max_streak=max(max_streak,streak)
            else: streak=0
        total=sum(rs); best=max(rs,default=0.0); loss_abs=-sum(losses)
        m=ResearchMetrics(outcome_count=len(self.outcomes),filled_count=len(filled),win_count=len(wins),loss_count=len(losses),flat_count=sum(r==0 for r in rs),ambiguous_count=sum(o.ambiguous for o in self.outcomes),no_fill_count=len(self.outcomes)-len(filled),unique_event_count=len(self.events),unique_cluster_count=len(self.clusters),fill_rate=len(filled)/len(self.outcomes) if self.outcomes else 0.0,win_rate=len(wins)/len(filled) if filled else 0.0,average_win_r=sum(wins)/len(wins) if wins else 0.0,average_loss_r=sum(losses)/len(losses) if losses else 0.0,expectancy_r=total/len(filled) if filled else 0.0,standard_deviation_r=stdev(rs) if len(rs)>1 else 0.0,profit_factor=sum(wins)/loss_abs if loss_abs>0 else (1e9 if wins else 0.0),total_net_r=total,maximum_drawdown_r=max_dd,maximum_runup_r=max_ru,average_mfe_r=sum(o.mfe_r for o in filled)/len(filled) if filled else 0.0,average_mae_r=sum(o.mae_r for o in filled)/len(filled) if filled else 0.0,average_holding_seconds=sum(o.holding_seconds for o in filled)/len(filled) if filled else 0.0,best_trade_r=best,worst_trade_r=min(rs,default=0.0),best_trade_share=best/total if total>0 and best>0 else 0.0,maximum_consecutive_losses=max_streak,fold_survival_score=fold_survival,cost_survival_score=cost_survival,stability_score=stability)
        return m.with_hash()
