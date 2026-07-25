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

def _latest_closed(
    provider: MT5Provider,
    symbol: str,
    now: datetime,
    retry_count: int,
    retry_delay_seconds: float,
) -> datetime:
    """Return the close time of the newest fully closed M1 bar.

    MetaTrader numbers bars from the present into the past: position zero is
    the current bar and position one is the immediately preceding bar.  The
    adapter therefore treats every row returned from ``start_pos=1`` as closed
    by provider contract.  It must not reclassify that bar with the workstation
    wall clock because terminal data can be ahead of or behind a misconfigured
    local clock even when the broker history is valid.

    ``now`` remains in the signature for API compatibility and deterministic
    tests, but it is deliberately not used as closure authority.
    """

    del now
    attempts: list[dict[str, Any]] = []

    for attempt in range(retry_count + 1):
        rows = provider.copy_rates_from_pos(symbol, 1, 10)
        row_count = 0 if rows is None else len(rows)

        if row_count > 0:
            opens: list[int] = []
            for row in rows:
                try:
                    opens.append(int(row["time"]))
                except (KeyError, TypeError, ValueError, OverflowError):
                    continue
            if opens:
                return datetime.fromtimestamp(max(opens) + 60, timezone.utc)

        attempts.append(
            {
                "attempt": attempt + 1,
                "returned_count": row_count,
                "last_error": provider.last_error(),
            }
        )

        if attempt < retry_count:
            time.sleep(retry_delay_seconds * (attempt + 1))

    raise RTHPMT5Error(
        "MT5_NO_CLOSED_M1_BAR",
        f"No closed M1 bar available for {symbol} after history synchronization retries",
        {"attempts": attempts, "start_pos": 1, "count": 10},
    )

def resolve_range(provider: MT5Provider, primary: ResolvedSymbol, secondary: ResolvedSymbol, history, now: datetime) -> tuple[datetime,datetime]:
    latest_common_end = min(
        _latest_closed(provider, primary.broker_symbol, now, history.retry_count, history.retry_delay_seconds),
        _latest_closed(provider, secondary.broker_symbol, now, history.retry_count, history.retry_delay_seconds),
    )

    if history.mode=='EXPLICIT_UTC_RANGE':
        start=datetime.fromisoformat(history.start_utc.replace('Z','+00:00')).astimezone(timezone.utc)
        requested_end=datetime.fromisoformat(history.end_utc.replace('Z','+00:00')).astimezone(timezone.utc)
        end=min(requested_end, latest_common_end)
    else:
        end=latest_common_end
        start=end-timedelta(days=history.max_lookback_days)

    start=start.replace(second=0,microsecond=0)
    end=end.replace(second=0,microsecond=0)
    if start>=end:
        raise RTHPMT5Error('MT5_RANGE_INVALID','Resolved common range is empty')
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
