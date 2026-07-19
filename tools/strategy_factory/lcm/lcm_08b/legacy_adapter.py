from __future__ import annotations
from dataclasses import asdict
import pandas as pd
from .models import ContextConfig
from .context_core import detect_occurrences

def outcome_projection(df:pd.DataFrame,start:int,horizon:int,bias:str)->dict:
    end=min(len(df)-1,start+max(1,horizon));entry=float(df.at[start,"close"]);best_mfe=best_mae=0.0;bars_to_mfe=bars_to_mae=0
    for k in range(start,end+1):
        if bias=="BUY":mfe=float(df.at[k,"high"]-entry);mae=float(entry-df.at[k,"low"])
        else:mfe=float(entry-df.at[k,"low"]);mae=float(df.at[k,"high"]-entry)
        if mfe>best_mfe:best_mfe,bars_to_mfe=mfe,k-start
        if mae>best_mae:best_mae,bars_to_mae=mae,k-start
    ret=float(df.at[end,"close"]-entry) if bias=="BUY" else float(entry-df.at[end,"close"])
    return {"entry_close":entry,"mfe_points":best_mfe,"mae_points":best_mae,"return_points":ret,"bars_to_mfe":bars_to_mfe,"bars_to_mae":bars_to_mae}

def run_legacy_compatible(a,b,cfg:ContextConfig,outcome_horizon_bars:int=12)->list[dict]:
    aa,bb,events=detect_occurrences(a,b,cfg);rows=[]
    for index,event in enumerate(events,1):
        row=asdict(event);row.pop("reason_code")
        origin=aa if event.origin_symbol==cfg.symbol_a else bb
        row={"event_id":index,"pair_label":cfg.pair_label,**row}
        row.update(outcome_projection(origin,aa.index[aa["time"]==pd.Timestamp(event.valid_from_time)][0] if event.origin_symbol==cfg.symbol_a else bb.index[bb["time"]==pd.Timestamp(event.valid_from_time)][0],outcome_horizon_bars,event.suggested_bias))
        row["note"]="origin took reference; destination failed inside lag"
        # Match the legacy dataclass field order exactly.
        order=["event_id","pair_label","origin_symbol","destination_symbol","bar_index","evaluation_time","valid_from_time","valid_until_time","side","suggested_bias","level_family","trigger_mode","step_every_bars","step_offset_bars","destination_lag_bars","signal_valid_bars","origin_ref_price","destination_ref_price","origin_ref_time","destination_ref_time","origin_ref_index","destination_ref_index","origin_break_points","destination_break_points","divergence_gap_points","destination_late_confirmed","destination_confirm_time","entry_close","mfe_points","mae_points","return_points","bars_to_mfe","bars_to_mae","note"]
        rows.append({k:row[k] for k in order})
    return rows
