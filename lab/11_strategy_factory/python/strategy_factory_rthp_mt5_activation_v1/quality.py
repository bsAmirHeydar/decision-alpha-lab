from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime,timezone
from zoneinfo import ZoneInfo
from .acquire import AcquisitionResult
from .canonical import sha256_material

NY=ZoneInfo('America/New_York'); MINUTE=60_000
@dataclass(frozen=True,slots=True)
class QualityResult:
    status: str; common_start_ms: int; common_end_ms: int; primary_bars: tuple; secondary_bars: tuple; report: dict

def _weekly_closed(ms:int)->bool:
    d=datetime.fromtimestamp(ms/1000,timezone.utc).astimezone(NY); wd=d.weekday(); minute=d.hour*60+d.minute
    return wd==4 and minute>=17*60 or wd==5 or wd==6 and minute<18*60

def validate_pair(primary: AcquisitionResult, secondary: AcquisitionResult, policy, minimum_common_days: int = 0) -> QualityResult:
    p={x.bar_open_time_utc_ms:x for x in primary.bars}; s={x.bar_open_time_utc_ms:x for x in secondary.bars}
    common=sorted(set(p)&set(s))
    if not common: raise ValueError('no common M1 history')
    start=max(min(p),min(s)); end=min(max(x.bar_close_time_utc_ms for x in p.values()),max(x.bar_close_time_utc_ms for x in s.values()))
    expected=list(range(start,end,MINUTE)); p_missing=[t for t in expected if t not in p and not _weekly_closed(t)]; s_missing=[t for t in expected if t not in s and not _weekly_closed(t)]
    p_only=sorted(set(p_missing)-set(s_missing)); s_only=sorted(set(s_missing)-set(p_missing)); joint=sorted(set(p_missing)&set(s_missing))
    ratio=(len(p_only)+len(s_only))/max(1,2*len(expected))
    blockers=[]
    if len(common)<policy.minimum_common_bars: blockers.append('INSUFFICIENT_COMMON_M1_BARS')
    common_duration_days = (max(common) + MINUTE - min(common)) / 86_400_000
    if minimum_common_days > 0 and common_duration_days < minimum_common_days:
        blockers.append('INSUFFICIENT_COMMON_HISTORY_DAYS')
    if ratio>policy.max_symbol_specific_gap_ratio: blockers.append('SYMBOL_SPECIFIC_GAP_RATIO_EXCEEDED')
    # Long unexplained weekday gaps block; short joint no-quote gaps are declared.
    def max_run(values):
        best=run=0; prev=None
        for t in values:
            run=run+1 if prev is not None and t-prev==MINUTE else 1; best=max(best,run); prev=t
        return best
    primary_only_max_run = max_run(p_only)
    secondary_only_max_run = max_run(s_only)
    joint_max_run = max_run(joint)
    if max(primary_only_max_run, secondary_only_max_run) > policy.max_unexplained_gap_minutes:
        blockers.append('UNEXPLAINED_SYMBOL_SPECIFIC_GAP_EXCEEDS_POLICY')
    if joint_max_run>policy.max_joint_gap_minutes: blockers.append('JOINT_GAP_EXCEEDS_POLICY')
    status='BLOCKED' if blockers else ('PASS_WITH_DECLARED_NON_CRITICAL_GAPS' if p_missing or s_missing else 'PASS')
    common_start=min(common); common_end=max(common)+MINUTE
    report={'report_id':'RTHP_MT5_M1_QUALITY_V1','schema_version':'1.0.0','status':status,'blockers':blockers,'canonical_source_timeframe':'M1_CLOSED_BARS',
            'sub_m1_source_allowed':False,'synthetic_ticks_allowed':False,'primary_bar_count':len(p),'secondary_bar_count':len(s),'common_bar_count':len(common),
            'common_start_utc_ms':common_start,'common_end_utc_ms':common_end,'primary_missing_open_minutes':len(p_missing),'secondary_missing_open_minutes':len(s_missing),
            'primary_only_gap_count':len(p_only),'secondary_only_gap_count':len(s_only),'joint_gap_count':len(joint),
            'max_primary_only_gap_run_minutes':primary_only_max_run,'max_secondary_only_gap_run_minutes':secondary_only_max_run,
            'max_joint_gap_run_minutes':joint_max_run,'common_duration_days':common_duration_days,
            'minimum_common_days_required':minimum_common_days,'symbol_specific_gap_ratio':ratio,
            'm15_missingness_is_unconfirmed':True,'forward_fill_allowed':False}
    report['report_digest']=sha256_material(report)
    return QualityResult(status,common_start,common_end,tuple(x for x in primary.bars if common_start<=x.bar_open_time_utc_ms and x.bar_close_time_utc_ms<=common_end),
                         tuple(x for x in secondary.bars if common_start<=x.bar_open_time_utc_ms and x.bar_close_time_utc_ms<=common_end),report)
