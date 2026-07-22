from __future__ import annotations
import time
from dataclasses import dataclass
from datetime import datetime,timedelta,timezone
from typing import Any
from .canonical import sha256_material
from .errors import RTHPMT5Error
from .m1_schema import CanonicalM1Bar, normalize_rate
from .provider import MT5Provider
from .symbols import ResolvedSymbol

@dataclass(frozen=True,slots=True)
class AcquisitionResult:
    symbol: ResolvedSymbol; bars: tuple[CanonicalM1Bar,...]; receipts: tuple[dict[str,Any],...]

def _latest_closed(provider: MT5Provider, symbol: str, now: datetime) -> datetime:
    rows=provider.copy_rates_from_pos(symbol,0,10)
    if rows is None: raise RTHPMT5Error('MT5_LATEST_BAR_FAILED',f'Could not read latest M1 bars for {symbol}',{'last_error':provider.last_error()})
    opens=sorted(int(row['time']) for row in rows)
    now_s=int(now.timestamp())
    closed=[x for x in opens if x+60<=now_s]
    if not closed: raise RTHPMT5Error('MT5_NO_CLOSED_M1_BAR',f'No closed M1 bar available for {symbol}')
    return datetime.fromtimestamp(max(closed)+60,timezone.utc)

def resolve_range(provider: MT5Provider, primary: ResolvedSymbol, secondary: ResolvedSymbol, history, now: datetime) -> tuple[datetime,datetime]:
    if history.mode=='EXPLICIT_UTC_RANGE':
        start=datetime.fromisoformat(history.start_utc.replace('Z','+00:00')).astimezone(timezone.utc); end=datetime.fromisoformat(history.end_utc.replace('Z','+00:00')).astimezone(timezone.utc)
    else:
        end=min(_latest_closed(provider,primary.broker_symbol,now),_latest_closed(provider,secondary.broker_symbol,now))
        start=end-timedelta(days=history.max_lookback_days)
    start=start.replace(second=0,microsecond=0); end=end.replace(second=0,microsecond=0)
    # Never request or materialize the currently forming M1 bar. An explicit
    # future end is safely capped at the latest fully closed UTC minute.
    latest_closed_minute = now.astimezone(timezone.utc).replace(second=0, microsecond=0)
    end = min(end, latest_closed_minute)
    if start>=end: raise RTHPMT5Error('MT5_RANGE_INVALID','Resolved common range is empty')
    return start,end

def acquire_symbol(provider: MT5Provider, symbol: ResolvedSymbol, start: datetime, end: datetime, history, terminal_id: str, revision: str) -> AcquisitionResult:
    bars: dict[int,CanonicalM1Bar]={}; receipts=[]; cursor=start; seq=0
    while cursor<end:
        chunk_end=min(end,cursor+timedelta(days=history.chunk_days)); request_start=max(start,cursor-timedelta(minutes=history.overlap_minutes))
        rows=None; errors=[]
        for attempt in range(history.retry_count+1):
            rows=provider.copy_rates_range(symbol.broker_symbol,request_start,chunk_end)
            if rows is not None: break
            errors.append(provider.last_error())
            if attempt<history.retry_count: time.sleep(history.retry_delay_seconds*(attempt+1))
        if rows is None: raise RTHPMT5Error('MT5_HISTORY_REQUEST_FAILED',f'M1 history request failed for {symbol.broker_symbol}',{'errors':errors})
        count=0
        for row in rows:
            bar=normalize_rate(row,symbol.broker_symbol,symbol.canonical_instrument_id,float(symbol.metadata['trade_tick_size']),terminal_id,revision,seq); seq+=1
            if not (int(start.timestamp()*1000)<=bar.bar_open_time_utc_ms and bar.bar_close_time_utc_ms<=int(end.timestamp()*1000)): continue
            existing=bars.get(bar.bar_open_time_utc_ms)
            if existing is not None and existing!=bar: raise RTHPMT5Error('MT5_CONFLICTING_OVERLAP_BAR','Conflicting bar in overlap',{'symbol':symbol.broker_symbol,'open_ms':bar.bar_open_time_utc_ms})
            bars[bar.bar_open_time_utc_ms]=bar; count+=1
        receipts.append({'symbol':symbol.broker_symbol,'request_start_utc':request_start.isoformat(),'request_end_utc':chunk_end.isoformat(),'returned_count':len(rows),
                         'accepted_count':count,'last_error':provider.last_error(),'attempt_count':len(errors)+1})
        cursor=chunk_end
    ordered=tuple(bars[k] for k in sorted(bars))
    if not ordered: raise RTHPMT5Error('MT5_NO_M1_HISTORY',f'No M1 bars acquired for {symbol.broker_symbol}')
    return AcquisitionResult(symbol,ordered,tuple(receipts))
