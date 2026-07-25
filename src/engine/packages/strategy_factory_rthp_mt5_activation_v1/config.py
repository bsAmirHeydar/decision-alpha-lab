from __future__ import annotations
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .canonical import sha256_material

@dataclass(frozen=True, slots=True)
class TerminalConfig:
    path: str | None = None
    timeout_ms: int = 60_000
    portable: bool = False
    require_connected: bool = True

@dataclass(frozen=True, slots=True)
class HistoryConfig:
    mode: str = "AUTO_COMMON_HISTORY"
    start_utc: str | None = None
    end_utc: str | None = None
    max_lookback_days: int = 730
    minimum_common_days: int = 30
    chunk_days: int = 14
    overlap_minutes: int = 2
    retry_count: int = 3
    retry_delay_seconds: float = 1.0

@dataclass(frozen=True, slots=True)
class QualityConfig:
    minimum_common_bars: int = 10_000
    max_symbol_specific_gap_ratio: float = 0.02
    max_joint_gap_minutes: int = 240
    max_unexplained_gap_minutes: int = 15
    require_exact_m15_coverage: bool = True
    reject_sub_m1: bool = True
    drop_incomplete_current_bar: bool = True
    session_calendar_profile: str = "AUTO"
    max_scheduled_closure_minutes: int = 1_440
    require_scheduled_closure_boundary_bars: bool = True

@dataclass(frozen=True, slots=True)
class TrainConfig:
    enabled: bool = True
    selected_task_ids: tuple[str,...] = ()
    family_filter: tuple[str,...] = ()
    minimum_mature_rows: int = 24
    max_rows: int = 2_000_000
    max_memory_mb: int = 8192
    max_wall_seconds: float = 3600.0
    seed: int = 1701

@dataclass(frozen=True, slots=True)
class MT5ActivationConfig:
    schema_version: str
    run_id: str
    output_root: Path
    primary_symbol: str
    secondary_symbol: str
    canonical_primary_id: str
    canonical_secondary_id: str
    terminal: TerminalConfig = field(default_factory=TerminalConfig)
    history: HistoryConfig = field(default_factory=HistoryConfig)
    quality: QualityConfig = field(default_factory=QualityConfig)
    train: TrainConfig = field(default_factory=TrainConfig)
    source_revision: str = "R1"
    contract_roll_policy: str = "NO_IMPLICIT_STITCHING_V1"
    entitlement_id: str = "LOCAL_MT5_TERMINAL_SESSION"

    @property
    def digest(self): return sha256_material(self)


def _dt(value: str | None) -> datetime | None:
    if value is None: return None
    v=value.replace('Z','+00:00'); d=datetime.fromisoformat(v)
    if d.tzinfo is None: raise ValueError('history timestamps must include UTC offset')
    return d.astimezone(timezone.utc)


def load_mt5_activation_config(path: str|Path) -> MT5ActivationConfig:
    p=Path(path).resolve(); raw=json.loads(p.read_text(encoding='utf-8'))
    if raw.get('schema_version')!='1.0.0': raise ValueError('unsupported MT5 activation schema_version')
    symbols=raw['symbols']; primary=str(symbols['primary']).strip(); secondary=str(symbols['secondary']).strip()
    if not primary or not secondary or primary==secondary: raise ValueError('two distinct non-empty symbols are required')
    tr=raw.get('terminal',{}); hr=raw.get('history',{}); qr=raw.get('quality',{}); train=raw.get('train',{})
    history=HistoryConfig(str(hr.get('mode','AUTO_COMMON_HISTORY')),hr.get('start_utc'),hr.get('end_utc'),int(hr.get('max_lookback_days',730)),
                          int(hr.get('minimum_common_days',30)),int(hr.get('chunk_days',14)),int(hr.get('overlap_minutes',2)),
                          int(hr.get('retry_count',3)),float(hr.get('retry_delay_seconds',1.0)))
    if history.mode not in {'AUTO_COMMON_HISTORY','EXPLICIT_UTC_RANGE'}: raise ValueError('unsupported history mode')
    start,end=_dt(history.start_utc),_dt(history.end_utc)
    if history.mode=='EXPLICIT_UTC_RANGE' and (start is None or end is None or start>=end): raise ValueError('explicit UTC range is invalid')
    base=p.parent; out=Path(raw.get('output_root',''))
    if not str(out): raise ValueError('output_root is required')
    if not out.is_absolute(): out=(base/out).resolve()
    config=MT5ActivationConfig('1.0.0',str(raw.get('run_id','AUTO')),out,primary,secondary,
        str(symbols.get('canonical_primary_id',primary)),str(symbols.get('canonical_secondary_id',secondary)),
        TerminalConfig(tr.get('path'),int(tr.get('timeout_ms',60000)),bool(tr.get('portable',False)),bool(tr.get('require_connected',True))),
        history,
        QualityConfig(int(qr.get('minimum_common_bars',10000)),float(qr.get('max_symbol_specific_gap_ratio',0.02)),
                      int(qr.get('max_joint_gap_minutes',240)),int(qr.get('max_unexplained_gap_minutes',15)),
                      bool(qr.get('require_exact_m15_coverage',True)),bool(qr.get('reject_sub_m1',True)),bool(qr.get('drop_incomplete_current_bar',True)),
                      str(qr.get('session_calendar_profile','AUTO')).upper(),int(qr.get('max_scheduled_closure_minutes',1440)),
                      bool(qr.get('require_scheduled_closure_boundary_bars',True))),
        TrainConfig(bool(train.get('enabled',True)),tuple(str(x) for x in train.get('selected_task_ids',())),tuple(str(x) for x in train.get('family_filter',())),
                    int(train.get('minimum_mature_rows',24)),int(train.get('max_rows',2000000)),int(train.get('max_memory_mb',8192)),
                    float(train.get('max_wall_seconds',3600.0)),int(train.get('seed',1701))),
        str(raw.get('source_revision','R1')),str(raw.get('contract_roll_policy','NO_IMPLICIT_STITCHING_V1')),
        str(raw.get('entitlement_id','LOCAL_MT5_TERMINAL_SESSION')))
    if not config.quality.reject_sub_m1: raise ValueError('canonical MT5 profile must reject sub-M1 data')
    if config.quality.session_calendar_profile not in {'AUTO','WEEKLY_ONLY_V1','US_INDEX_CFD_NY_V1'}:
        raise ValueError('unsupported session calendar profile')
    if config.quality.max_scheduled_closure_minutes < config.quality.max_joint_gap_minutes:
        raise ValueError('max_scheduled_closure_minutes must be at least max_joint_gap_minutes')
    return config


def build_symbol_selection_config(
    primary_symbol: str,
    secondary_symbol: str,
    output_root: Path,
    *,
    terminal_path: str | None = None,
    lookback_days: int = 730,
    minimum_common_days: int = 30,
    train_enabled: bool = True,
    selected_task_ids: tuple[str, ...] = (),
    family_filter: tuple[str, ...] = (),
) -> MT5ActivationConfig:
    primary = primary_symbol.strip()
    secondary = secondary_symbol.strip()
    if not primary or not secondary or primary.casefold() == secondary.casefold():
        raise ValueError("two distinct non-empty symbols are required")
    if lookback_days < minimum_common_days or minimum_common_days < 1:
        raise ValueError("lookback_days must be at least minimum_common_days >= 1")
    return MT5ActivationConfig(
        "1.0.0",
        "AUTO",
        output_root.resolve(),
        primary,
        secondary,
        primary,
        secondary,
        TerminalConfig(terminal_path, 60_000, False, True),
        HistoryConfig("AUTO_COMMON_HISTORY", None, None, lookback_days, minimum_common_days, 14, 2, 3, 1.0),
        QualityConfig(),
        TrainConfig(True if train_enabled else False, selected_task_ids, family_filter),
        "MT5_AUTO_R1",
        "NO_IMPLICIT_STITCHING_V1",
        "LOCAL_MT5_TERMINAL_SESSION",
    )
