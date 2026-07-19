from __future__ import annotations
import pandas as pd
from .models import ContextConfig,ContextOccurrence,Side
from .data_adapter import normalize_bars,align_bars

def minute_of_day(ts:pd.Timestamp)->int: return int(ts.hour)*60+int(ts.minute)

def in_session(ts:pd.Timestamp,start_minute:int,end_minute:int)->bool:
    m=minute_of_day(ts)
    if start_minute==end_minute:return True
    if start_minute<end_minute:return start_minute<=m<end_minute
    return m>=start_minute or m<end_minute

def reference_levels(df:pd.DataFrame,i:int,family:str,rolling:int,session_start:int,session_end:int):
    if i<=0 or i>=len(df): return None
    if family=="previous_candle":
        j=i-1
        return {"high":df.at[j,"high"],"low":df.at[j,"low"],"high_i":j,"low_i":j,"high_time":df.at[j,"time"],"low_time":df.at[j,"time"]}
    if family=="rolling":
        start=max(0,i-max(1,rolling));w=df.iloc[start:i]
        if w.empty:return None
        hi_i=int(w["high"].idxmax());lo_i=int(w["low"].idxmin())
        return {"high":df.at[hi_i,"high"],"low":df.at[lo_i,"low"],"high_i":hi_i,"low_i":lo_i,"high_time":df.at[hi_i,"time"],"low_time":df.at[lo_i,"time"]}
    if family=="current_session":
        day=df.at[i,"time"].date();mask=[False]*i
        for k in range(i):
            ts=df.at[k,"time"];mask[k]=ts.date()==day and in_session(ts,session_start,session_end)
        w=df.iloc[:i][mask]
        if w.empty:return None
        hi_i=int(w["high"].idxmax());lo_i=int(w["low"].idxmin())
        return {"high":df.at[hi_i,"high"],"low":df.at[lo_i,"low"],"high_i":hi_i,"low_i":lo_i,"high_time":df.at[hi_i,"time"],"low_time":df.at[lo_i,"time"]}
    if family=="previous_session":
        current_day=df.at[i,"time"].date();prev_days=[]
        for k in range(i):
            ts=df.at[k,"time"]
            if ts.date()!=current_day and in_session(ts,session_start,session_end):prev_days.append(ts.date())
        if not prev_days:return None
        prev_day=prev_days[-1];mask=[]
        for k in range(i):
            ts=df.at[k,"time"];mask.append(ts.date()==prev_day and in_session(ts,session_start,session_end))
        w=df.iloc[:i][mask]
        if w.empty:return None
        hi_i=int(w["high"].idxmax());lo_i=int(w["low"].idxmin())
        return {"high":df.at[hi_i,"high"],"low":df.at[lo_i,"low"],"high_i":hi_i,"low_i":lo_i,"high_time":df.at[hi_i,"time"],"low_time":df.at[lo_i,"time"]}
    raise ValueError(f"unknown level family: {family}")

def triggered(row:pd.Series,side:Side,mode:str,level:float)->tuple[bool,float]:
    if side=="HIGH":
        if mode=="wick_touch" and row.high>=level:return True,float(row.high-level)
        if mode=="close_break" and row.close>level:return True,float(row.close-level)
        if mode=="hunt_reject_close" and row.high>=level and row.close<level:return True,float(row.high-level)
    else:
        if mode=="wick_touch" and row.low<=level:return True,float(level-row.low)
        if mode=="close_break" and row.close<level:return True,float(level-row.close)
        if mode=="hunt_reject_close" and row.low<=level and row.close>level:return True,float(level-row.low)
    return False,0.0

def _detect_direction(origin_symbol,destination_symbol,origin,destination,cfg:ContextConfig):
    out=[];n=min(len(origin),len(destination))
    for i in range(max(1,cfg.start_after_bars),n-cfg.destination_lag_bars):
        if (i-cfg.step_offset_bars)%max(1,cfg.step_every_bars)!=0:continue
        ol=reference_levels(origin,i,cfg.level_family,cfg.rolling_lookback,cfg.session_start_minute,cfg.session_end_minute)
        dl=reference_levels(destination,i,cfg.level_family,cfg.rolling_lookback,cfg.session_start_minute,cfg.session_end_minute)
        if not ol or not dl:continue
        for side in ("HIGH","LOW"):
            origin_level=float(ol["high"] if side=="HIGH" else ol["low"]);dest_level=float(dl["high"] if side=="HIGH" else dl["low"])
            origin_hit,obp=triggered(origin.iloc[i],side,cfg.trigger_mode,origin_level)
            if not origin_hit:continue
            dest_hit=False;dest_bp=0.0
            for j in range(i,min(n,i+cfg.destination_lag_bars+1)):
                dest_hit,dest_bp=triggered(destination.iloc[j],side,cfg.trigger_mode,dest_level)
                if dest_hit:break
            if dest_hit:continue
            valid_from=min(n-1,i+cfg.destination_lag_bars);valid_until=min(n-1,valid_from+max(1,cfg.signal_valid_bars))
            late=False;late_time=""
            for j in range(valid_from+1,valid_until+1):
                late,_=triggered(destination.iloc[j],side,cfg.trigger_mode,dest_level)
                if late:late_time=str(destination.at[j,"time"]);break
            out.append(ContextOccurrence(
                origin_symbol=origin_symbol,destination_symbol=destination_symbol,bar_index=i,
                evaluation_time=str(origin.at[i,"time"]),valid_from_time=str(origin.at[valid_from,"time"]),valid_until_time=str(origin.at[valid_until,"time"]),
                side=f"{side}_DIVERGENCE",suggested_bias="SELL" if side=="HIGH" else "BUY",
                level_family=cfg.level_family,trigger_mode=cfg.trigger_mode,step_every_bars=cfg.step_every_bars,step_offset_bars=cfg.step_offset_bars,
                destination_lag_bars=cfg.destination_lag_bars,signal_valid_bars=cfg.signal_valid_bars,
                origin_ref_price=origin_level,destination_ref_price=dest_level,
                origin_ref_time=str(ol["high_time"] if side=="HIGH" else ol["low_time"]),destination_ref_time=str(dl["high_time"] if side=="HIGH" else dl["low_time"]),
                origin_ref_index=int(ol["high_i"] if side=="HIGH" else ol["low_i"]),destination_ref_index=int(dl["high_i"] if side=="HIGH" else dl["low_i"]),
                origin_break_points=obp,destination_break_points=dest_bp,divergence_gap_points=abs(origin_level-dest_level),
                destination_late_confirmed=late,destination_confirm_time=late_time,reason_code="ORIGIN_TOOK_REFERENCE_DESTINATION_FAILED_WITHIN_LAG"))
    return out

def detect_occurrences(a,b,cfg:ContextConfig):
    a=normalize_bars(a);b=normalize_bars(b);a,b=align_bars(a,b);events=[]
    if cfg.scan_a_as_origin:events.extend(_detect_direction(cfg.symbol_a,cfg.symbol_b,a,b,cfg))
    if cfg.scan_b_as_origin:events.extend(_detect_direction(cfg.symbol_b,cfg.symbol_a,b,a,cfg))
    return a,b,events
