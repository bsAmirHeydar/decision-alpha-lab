from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Protocol
from .errors import RTHPMT5Error

class MT5Provider(Protocol):
    package_version: str
    def initialize(self, path: str|None, timeout_ms: int, portable: bool) -> bool: ...
    def shutdown(self) -> None: ...
    def last_error(self) -> Any: ...
    def terminal_info(self) -> Any: ...
    def account_info(self) -> Any: ...
    def version(self) -> Any: ...
    def symbols_get(self) -> Any: ...
    def symbol_select(self, symbol: str, enable: bool) -> bool: ...
    def symbol_info(self, symbol: str) -> Any: ...
    def copy_rates_range(self, symbol: str, date_from: datetime, date_to: datetime) -> Any: ...
    def copy_rates_from_pos(self, symbol: str, start_pos: int, count: int) -> Any: ...

class MetaTrader5Provider:
    def __init__(self):
        try:
            import MetaTrader5 as mt5
        except ImportError as exc:
            raise RTHPMT5Error('MT5_PYTHON_PACKAGE_NOT_INSTALLED','MetaTrader5 Python package is not installed') from exc
        self._mt5=mt5; self.package_version=str(getattr(mt5,'__version__','UNKNOWN'))
    def initialize(self,path,timeout_ms,portable):
        kwargs={'timeout':timeout_ms,'portable':portable}
        return bool(self._mt5.initialize(path,**kwargs) if path else self._mt5.initialize(**kwargs))
    def shutdown(self): self._mt5.shutdown()
    def last_error(self): return self._mt5.last_error()
    def terminal_info(self): return self._mt5.terminal_info()
    def account_info(self): return self._mt5.account_info()
    def version(self): return self._mt5.version()
    def symbols_get(self): return self._mt5.symbols_get()
    def symbol_select(self,symbol,enable): return bool(self._mt5.symbol_select(symbol,enable))
    def symbol_info(self,symbol): return self._mt5.symbol_info(symbol)
    def copy_rates_range(self,symbol,date_from,date_to): return self._mt5.copy_rates_range(symbol,self._mt5.TIMEFRAME_M1,date_from,date_to)
    def copy_rates_from_pos(self,symbol,start_pos,count): return self._mt5.copy_rates_from_pos(symbol,self._mt5.TIMEFRAME_M1,start_pos,count)

def as_mapping(value: Any) -> dict[str,Any]:
    if value is None: return {}
    if hasattr(value,'_asdict'): return dict(value._asdict())
    if isinstance(value,dict): return dict(value)
    return {k:getattr(value,k) for k in dir(value) if not k.startswith('_') and not callable(getattr(value,k,None))}
