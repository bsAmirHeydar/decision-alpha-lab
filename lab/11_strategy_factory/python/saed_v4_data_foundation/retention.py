from __future__ import annotations
from dataclasses import dataclass
from datetime import timedelta
from .canonical import parse_time
from .enums import RetentionClass
from .errors import AccessDenied
@dataclass(frozen=True)
class RetentionPolicy:
    retention_class:RetentionClass; minimum_days:int; legal_hold:bool=False
    def deletable(self,created_at:str,now:str)->bool:
        if self.legal_hold or self.retention_class==RetentionClass.PERMANENT: return False
        return parse_time(now)-parse_time(created_at)>=timedelta(days=self.minimum_days)
    def require_deletable(self,created_at:str,now:str):
        if not self.deletable(created_at,now): raise AccessDenied('retention policy forbids deletion')
