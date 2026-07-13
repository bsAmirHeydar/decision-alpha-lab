from __future__ import annotations
class PortfolioError(ValueError):
    def __init__(self, code: str, message: str, details: dict | None = None):
        super().__init__(message); self.code=code; self.message=message; self.details=details or {}
    def as_dict(self): return {"code":self.code,"message":self.message,"details":self.details}
