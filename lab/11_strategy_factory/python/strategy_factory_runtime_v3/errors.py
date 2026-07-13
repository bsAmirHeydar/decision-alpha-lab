from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping

@dataclass
class RuntimeContractError(ValueError):
    code:str
    message:str
    details:Mapping[str,Any]|None=None
    def __str__(self)->str:
        return f"{self.code}: {self.message}" + (f" {dict(self.details)}" if self.details else "")

class BundleValidationError(RuntimeContractError): pass
class ExportUnavailableError(RuntimeContractError): pass
class ParityFailure(RuntimeContractError): pass
class ActivationError(RuntimeContractError): pass
class DuplicateDecisionError(RuntimeContractError): pass
