from __future__ import annotations
import hashlib
from dataclasses import dataclass
from typing import Any
from .errors import RTHPMT5Error
from .provider import MT5Provider, as_mapping

@dataclass(frozen=True, slots=True)
class TerminalReceipt:
    terminal_id: str
    package_version: str
    terminal_version: list[Any]
    connected: bool
    server: str
    account_identity_hash: str
    terminal_path: str
    data_path: str
    build: int

class TerminalSession:
    def __init__(self, provider: MT5Provider, path: str|None, timeout_ms: int, portable: bool, require_connected: bool):
        self.provider,self.path,self.timeout_ms,self.portable,self.require_connected=provider,path,timeout_ms,portable,require_connected
        self.receipt: TerminalReceipt|None=None
    def __enter__(self):
        if not self.provider.initialize(self.path,self.timeout_ms,self.portable):
            raise RTHPMT5Error('MT5_INITIALIZE_FAILED','Could not initialize MetaTrader 5',{'last_error':self.provider.last_error()})
        ti,ai,version=as_mapping(self.provider.terminal_info()),as_mapping(self.provider.account_info()),self.provider.version()
        if not ti or not ai or version is None: raise RTHPMT5Error('MT5_HEALTH_INFO_UNAVAILABLE','Terminal/account/version information unavailable')
        connected=bool(ti.get('connected',False))
        if self.require_connected and not connected: raise RTHPMT5Error('MT5_TERMINAL_NOT_CONNECTED','MetaTrader terminal is not connected')
        account_material=f"{ai.get('login','')}|{ai.get('server','')}".encode(); account_hash=hashlib.sha256(account_material).hexdigest()
        path=str(ti.get('path','')); data_path=str(ti.get('data_path','')); build=int(ti.get('build',version[1] if len(version)>1 else 0))
        terminal_id=hashlib.sha256(f"{path}|{data_path}|{ai.get('server','')}|{build}".encode()).hexdigest()[:24].upper()
        self.receipt=TerminalReceipt(terminal_id,str(self.provider.package_version),list(version),connected,str(ai.get('server','')),account_hash,path,data_path,build)
        return self
    def __exit__(self,*_): self.provider.shutdown()
