from __future__ import annotations
from dataclasses import dataclass,asdict
from typing import Literal
Side=Literal["HIGH","LOW"]
Bias=Literal["BUY","SELL"]
LevelFamily=Literal["previous_candle","rolling","current_session","previous_session"]
TriggerMode=Literal["wick_touch","close_break","hunt_reject_close"]

@dataclass(frozen=True)
class ContextConfig:
    pair_label:str="ES_NQ"
    symbol_a:str="ES"
    symbol_b:str="NQ"
    level_family:LevelFamily="current_session"
    trigger_mode:TriggerMode="wick_touch"
    rolling_lookback:int=20
    session_start_minute:int=570
    session_end_minute:int=960
    step_every_bars:int=1
    step_offset_bars:int=0
    destination_lag_bars:int=2
    signal_valid_bars:int=12
    start_after_bars:int=100
    scan_a_as_origin:bool=True
    scan_b_as_origin:bool=True

@dataclass(frozen=True)
class ContextOccurrence:
    origin_symbol:str
    destination_symbol:str
    bar_index:int
    evaluation_time:str
    valid_from_time:str
    valid_until_time:str
    side:str
    suggested_bias:str
    level_family:str
    trigger_mode:str
    step_every_bars:int
    step_offset_bars:int
    destination_lag_bars:int
    signal_valid_bars:int
    origin_ref_price:float
    destination_ref_price:float
    origin_ref_time:str
    destination_ref_time:str
    origin_ref_index:int
    destination_ref_index:int
    origin_break_points:float
    destination_break_points:float
    divergence_gap_points:float
    destination_late_confirmed:bool
    destination_confirm_time:str
    reason_code:str

    def to_dict(self): return asdict(self)
