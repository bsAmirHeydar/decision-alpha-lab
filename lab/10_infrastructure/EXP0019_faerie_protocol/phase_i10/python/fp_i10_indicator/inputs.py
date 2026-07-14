import re
from .contracts import IndicatorConfig
from .constants import *
from .canonical import stable_id
from .errors import FPI10Error

SYMBOL_RE=re.compile(r'^[A-Za-z0-9._-]{1,64}$')
def normalize_symbol(value:str)->str:
    v=value.strip().upper()
    if not SYMBOL_RE.fullmatch(v): raise FPI10Error('FP_IND_SYMBOL_INVALID','symbol contains unsupported characters')
    return v

def canonical_pair_id(a:str,b:str)->str:
    x,y=sorted((normalize_symbol(a),normalize_symbol(b)))
    return f'PAIR-{x}-{y}'

def build_config(*,context_id='FP-CONTEXT-001',context_epoch,primary_symbol,secondary_symbol,host_timeframe_minutes=5,timer_seconds=DEFAULT_TIMER_SECONDS,history_days=DEFAULT_HISTORY_DAYS,max_incremental_minutes=DEFAULT_MAX_INCREMENTAL_MINUTES,enable_state_buffers=True,enable_diagnostics=True,fail_init_on_blocked_manifest=True):
    p=normalize_symbol(primary_symbol); s=normalize_symbol(secondary_symbol)
    return IndicatorConfig(context_id,context_epoch,p,s,canonical_pair_id(p,s),host_timeframe_minutes,timer_seconds,history_days,max_incremental_minutes,bool(enable_state_buffers),bool(enable_diagnostics),bool(fail_init_on_blocked_manifest))
