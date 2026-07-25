from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
from .legacy_loader import load_legacy
from .legacy_adapter import run_legacy_compatible
from .models import ContextConfig
from .canonical import digest_object

HARD_FIELDS=("event_id","pair_label","origin_symbol","destination_symbol","bar_index","evaluation_time","valid_from_time","valid_until_time","side","suggested_bias","level_family","trigger_mode","step_every_bars","step_offset_bars","destination_lag_bars","signal_valid_bars","origin_ref_price","destination_ref_price","origin_ref_time","destination_ref_time","origin_ref_index","destination_ref_index","origin_break_points","destination_break_points","divergence_gap_points","destination_late_confirmed","destination_confirm_time","entry_close","mfe_points","mae_points","return_points","bars_to_mfe","bars_to_mae","note")

def legacy_rows(repo_root:Path,a:Path,b:Path,cfg:ContextConfig,horizon:int):
    m=load_legacy(repo_root);aa=m.load_bars(a);bb=m.load_bars(b);aa,bb=m.align(aa,bb);events=[]
    if cfg.scan_a_as_origin:events.extend(m.detect_origin_destination(cfg.pair_label,cfg.symbol_a,cfg.symbol_b,aa,bb,cfg.level_family,cfg.trigger_mode,cfg.rolling_lookback,cfg.session_start_minute,cfg.session_end_minute,cfg.step_every_bars,cfg.step_offset_bars,cfg.destination_lag_bars,cfg.signal_valid_bars,cfg.start_after_bars,horizon,len(events)+1))
    if cfg.scan_b_as_origin:events.extend(m.detect_origin_destination(cfg.pair_label,cfg.symbol_b,cfg.symbol_a,bb,aa,cfg.level_family,cfg.trigger_mode,cfg.rolling_lookback,cfg.session_start_minute,cfg.session_end_minute,cfg.step_every_bars,cfg.step_offset_bars,cfg.destination_lag_bars,cfg.signal_valid_bars,cfg.start_after_bars,horizon,len(events)+1))
    from dataclasses import asdict
    return [asdict(e) for e in events]

def compare_case(repo_root:Path,case:dict,fixture_root:Path)->dict:
    cfg=ContextConfig(**case["config"]);a=fixture_root/case["a_csv"];b=fixture_root/case["b_csv"];h=case.get("outcome_horizon_bars",12)
    legacy=legacy_rows(repo_root,a,b,cfg,h);canonical=run_legacy_compatible(a,b,cfg,h)
    mismatches=[]
    if len(legacy)!=len(canonical):mismatches.append({"dimension":"EVENT_COUNT","legacy":len(legacy),"canonical":len(canonical)})
    for i,(left,right) in enumerate(zip(legacy,canonical)):
        for field in HARD_FIELDS:
            if left.get(field)!=right.get(field):mismatches.append({"event_index":i,"field":field,"legacy":left.get(field),"canonical":right.get(field)})
    return {"case_id":case["case_id"],"case_type":case["case_type"],"status":"PASS" if not mismatches else "FAIL","legacy_event_count":len(legacy),"canonical_event_count":len(canonical),"legacy_digest":digest_object(legacy),"canonical_digest":digest_object(canonical),"mismatches":mismatches}
