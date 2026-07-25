from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Any
from .canonical import sha256_material
from .errors import RTHPMT5Error
from .provider import MT5Provider, as_mapping

@dataclass(frozen=True, slots=True)
class ResolvedSymbol:
    requested: str
    broker_symbol: str
    canonical_instrument_id: str
    metadata: dict[str,Any]
    metadata_digest: str

_ALLOWED=('name','description','path','digits','point','trade_tick_size','trade_contract_size','trade_calc_mode','trade_mode','currency_base','currency_profit','currency_margin','start_time','expiration_time','spread','spread_float','visible','select')

def _candidates(provider: MT5Provider, requested: str) -> list[str]:
    symbols=provider.symbols_get()
    if symbols is None: raise RTHPMT5Error('MT5_SYMBOL_ENUMERATION_FAILED','symbols_get failed',{'last_error':provider.last_error()})
    names=[str(as_mapping(x).get('name','')) for x in symbols]
    exact=[x for x in names if x==requested]
    if exact: return exact
    ci=[x for x in names if x.lower()==requested.lower()]
    if ci: return ci
    return []

def resolve_symbol(provider: MT5Provider, requested: str, canonical_id: str) -> ResolvedSymbol:
    candidates=_candidates(provider,requested)
    if len(candidates)!=1: raise RTHPMT5Error('MT5_SYMBOL_NOT_UNIQUELY_RESOLVED',f'Symbol {requested!r} did not resolve uniquely',{'candidates':candidates})
    symbol=candidates[0]
    if not provider.symbol_select(symbol,True): raise RTHPMT5Error('MT5_SYMBOL_SELECT_FAILED',f'Could not enable {symbol}',{'last_error':provider.last_error()})
    info=as_mapping(provider.symbol_info(symbol))
    if not info: raise RTHPMT5Error('MT5_SYMBOL_INFO_FAILED',f'Could not read metadata for {symbol}')
    meta={k:info.get(k) for k in _ALLOWED}; meta['canonical_instrument_id']=canonical_id
    tick_size=float(meta.get('trade_tick_size') or 0)
    if tick_size<=0: raise RTHPMT5Error('MT5_SYMBOL_TICK_SIZE_INVALID',f'Invalid trade tick size for {symbol}')
    return ResolvedSymbol(requested,symbol,canonical_id,meta,'sha256:'+sha256_material(meta))
