from dataclasses import dataclass
from .enums import *
from .errors import CapabilityError
@dataclass(frozen=True,slots=True)
class CompatibilityFinding: code:str;blocking:bool;message:str
@dataclass(frozen=True,slots=True)
class CompatibilityReport: trainer_key:str;task_key:str;dataset_id:str;compatible:bool;findings:tuple[CompatibilityFinding,...]
class CapabilityMatcher:
 @staticmethod
 def evaluate(d,t,s,b):
  f=[]
  def c(ok,code,msg):
   if not ok:f.append(CompatibilityFinding(code,True,msg))
  c(t.task_kind in d.supported_tasks,'unsupported_task','task unsupported')
  c(t.view_kind in d.supported_views,'unsupported_view','view unsupported')
  c(t.target_shape in d.supported_target_shapes,'unsupported_target_shape','target unsupported')
  c(s.tensor_kind in d.supported_tensors,'unsupported_tensor','tensor unsupported')
  c(s.view_kind is t.view_kind,'task_dataset_view_mismatch','view mismatch')
  c(s.target_shape is t.target_shape,'task_dataset_target_mismatch','target mismatch')
  c(s.row_count>=d.min_rows,'too_few_rows','too few rows')
  c(s.row_count<=b.max_rows,'row_budget_exceeded','row budget exceeded')
  c(len(s.feature_order)<=min(d.max_features,b.max_features),'too_many_features','too many features')
  c(s.output_count<=min(d.max_outputs,b.max_outputs),'too_many_outputs','too many outputs')
  if s.output_count>1 or len(t.output_names)>1:c(d.supports_multi_output,'multi_output_unsupported','multi output unsupported')
  if s.has_sample_weights or t.sample_weight_required:c(d.supports_sample_weight,'sample_weight_unsupported','weights unsupported')
  if s.has_missing_values:c(d.missingness_support is not MissingnessSupport.REJECT,'missingness_unsupported','missing values unsupported')
  if s.has_censoring or t.censoring is not CensoringSupport.NONE:c(t.censoring in d.censoring_support,'censoring_unsupported','censoring unsupported')
  if t.calibration_required:c(any(x is not CalibrationKind.NONE for x in d.calibration_kinds),'calibration_unsupported','calibration unsupported')
  c(b.device in d.devices or DeviceKind.AUTO in d.devices,'device_unsupported','device unsupported')
  c(b.precision in d.precisions,'precision_unsupported','precision unsupported')
  if b.deterministic_required:c(d.determinism is not DeterminismLevel.NONDETERMINISTIC,'determinism_unavailable','determinism unavailable')
  return CompatibilityReport(d.key,t.key,s.dataset_id,not f,tuple(f))
 @staticmethod
 def require(d,t,s,b):
  r=CapabilityMatcher.evaluate(d,t,s,b)
  if not r.compatible:raise CapabilityError('trainer_incompatible','trainer capability mismatch',{'findings':[x.code for x in r.findings]})
  return r
