from dataclasses import dataclass
from typing import Any,Mapping
@dataclass(frozen=True,slots=True)
class TrainerErrorContext: code:str; message:str; details:Mapping[str,Any]
class TrainerError(RuntimeError):
 def __init__(self,code,message,details=None): self.context=TrainerErrorContext(code,message,dict(details or {}));super().__init__(f'{code}: {message}')
class CapabilityError(TrainerError): pass
class LifecycleError(TrainerError): pass
class DataAccessError(TrainerError): pass
class ResourceBudgetError(TrainerError): pass
class ArtifactError(TrainerError): pass
class OrchestrationError(TrainerError): pass
class SerializationError(TrainerError): pass

class OrchestrationRunFailed(OrchestrationError):
 def __init__(self,code,message,trial_ledger=(),access_audit=(),telemetry=(),details=None):
  super().__init__(code,message,details);self.trial_ledger=tuple(trial_ledger);self.access_audit=tuple(access_audit);self.telemetry=tuple(telemetry)
