from __future__ import annotations
import math,statistics
from .canonical import canonical_sha256

def deterministic_trial_metrics(context_id:str,treatment_id:str,algorithm_id:str,fold_id:str,seed:int,decision_count:int=24)->dict[str,float]:
 key=int(canonical_sha256({'c':context_id,'t':treatment_id,'a':algorithm_id,'f':fold_id,'s':seed})[:16],16)
 edge=((key%2001)-1000)/5000.0
 win_rate=max(0.05,min(0.95,0.5+edge))
 mean_r=edge*2.5
 volatility=0.7+((key>>12)%700)/1000
 sharpe=mean_r/volatility*math.sqrt(max(1,decision_count))
 drawdown=-(0.4+((key>>24)%1600)/1000)
 calibration=abs(win_rate-(0.5+edge*0.8))
 turnover=1.0+((key>>32)%1200)/100
 return {'mean_net_r':mean_r,'win_rate':win_rate,'sharpe':sharpe,'max_drawdown_r':drawdown,'calibration_error':calibration,'turnover':turnover}

def aggregate_metrics(rows:list[dict[str,float]])->dict[str,float]:
 if not rows:return {}
 keys=sorted(set.intersection(*(set(x) for x in rows)))
 return {k:statistics.fmean(x[k] for x in rows) for k in keys}
