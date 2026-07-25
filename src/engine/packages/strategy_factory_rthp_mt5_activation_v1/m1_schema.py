from __future__ import annotations
import math
from dataclasses import asdict, dataclass
from typing import Any

MINUTE_MS=60_000
@dataclass(frozen=True,slots=True)
class CanonicalM1Bar:
    symbol: str; canonical_instrument_id: str; timeframe_seconds: int; bar_open_time_utc_ms: int; bar_close_time_utc_ms: int; known_time_utc_ms: int
    open: float; high: float; low: float; close: float; tick_volume: int; spread: int; real_volume: int; tick_size: float
    source_sequence: int; source_terminal_id: str; source_revision: str
    def to_dict(self): return asdict(self)

def normalize_rate(rate: Any, symbol: str, canonical_id: str, tick_size: float, terminal_id: str, revision: str, sequence: int) -> CanonicalM1Bar:
    r=dict(rate) if isinstance(rate,dict) else {name:rate[name].item() if hasattr(rate[name],'item') else rate[name] for name in rate.dtype.names}
    open_ms=int(r['time'])*1000; close_ms=open_ms+MINUTE_MS
    o,h,l,c=(float(r[k]) for k in ('open','high','low','close'))
    if not all(math.isfinite(x) and x>0 for x in (o,h,l,c)) or l>h or not l<=o<=h or not l<=c<=h: raise ValueError('invalid MT5 OHLC row')
    return CanonicalM1Bar(symbol,canonical_id,60,open_ms,close_ms,close_ms,o,h,l,c,int(r.get('tick_volume',0)),int(r.get('spread',0)),int(r.get('real_volume',0)),tick_size,int(r['time'])//60,terminal_id,revision)
