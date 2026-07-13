from __future__ import annotations
from typing import Any, Mapping
class PolicyError(ValueError):
    def __init__(self, code:str, message:str, details:Mapping[str,Any]|None=None):
        super().__init__(message); self.code=code; self.details=dict(details or {})
