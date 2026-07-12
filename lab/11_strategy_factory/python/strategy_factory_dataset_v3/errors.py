from __future__ import annotations

class DatasetError(ValueError):
    def __init__(self, code:str, message:str, evidence:dict|None=None):
        super().__init__(f"{code}: {message}")
        self.code=code; self.message=message; self.evidence=evidence or {}

class ContractError(DatasetError): pass
class CausalityError(DatasetError): pass
class MaturityError(DatasetError): pass
class LeakageError(DatasetError): pass
