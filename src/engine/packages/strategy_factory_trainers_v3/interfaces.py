from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import Any,Mapping
from .contracts import *
from .data_access import DataView
from .canonical import canonical_sha256
@dataclass(frozen=True,slots=True)
class FittedModel: trainer_key:str;task_key:str;feature_order:tuple[str,...];output_names:tuple[str,...];state:Mapping[str,Any];state_hash:str
@dataclass(frozen=True,slots=True)
class CalibrationState: kind:CalibrationKind;parameters:Mapping[str,float];state_hash:str
@dataclass(frozen=True,slots=True)
class ExplanationArtifact: kind:ExplainabilityKind;global_importance:Mapping[str,float];local_contributions:Mapping[str,tuple[float,...]];evidence_hash:str
class TrainerPlugin(ABC):
 @classmethod
 @abstractmethod
 def capability(cls):...
 @abstractmethod
 def configure(self,config,resources):...
 @abstractmethod
 def validate(self,task,schema):...
 @abstractmethod
 def fit(self,train:DataView):...
 @abstractmethod
 def predict(self,model,data,lineage):...
 def calibrate(self,model,data,kind):return CalibrationState(CalibrationKind.IDENTITY,{},canonical_sha256({'kind':'identity','model':model.state_hash}))
 def apply_calibration(self,batch,state):return batch
 def explain(self,model,data,kind):return ExplanationArtifact(ExplainabilityKind.NONE,{}, {},canonical_sha256({'model':model.state_hash,'rows':data.row_ids}))
 def export(self,model,fmt):
  if fmt is not ExportFormat.NATIVE_JSON:raise NotImplementedError(fmt.value)
  return self.serialize(model).encode()
 @abstractmethod
 def serialize(self,model):...
 @abstractmethod
 def load(self,payload):...
 def dispose(self):pass
