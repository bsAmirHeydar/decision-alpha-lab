from dataclasses import dataclass
from math import isfinite
from .canonical import canonical_sha256
from .contracts import TrainingRow,DatasetSchema,AccessAuditRecord
from .enums import SplitRole,AccessPurpose,OrchestrationPhase
from .errors import DataAccessError
_ALLOWED={SplitRole.TRAIN:{AccessPurpose.FIT,AccessPurpose.VALIDATE_SCHEMA},SplitRole.CALIBRATION:{AccessPurpose.CALIBRATE},SplitRole.THRESHOLD:{AccessPurpose.SELECT_THRESHOLD},SplitRole.OOF_HOLDOUT:{AccessPurpose.PREDICT_OOF,AccessPurpose.EXPLAIN},SplitRole.FINAL_TRAIN:{AccessPurpose.FIT},SplitRole.FINAL_CALIBRATION:{AccessPurpose.CALIBRATE},SplitRole.FINAL_THRESHOLD:{AccessPurpose.SELECT_THRESHOLD},SplitRole.FINAL_TEST:{AccessPurpose.PREDICT_FINAL_TEST,AccessPurpose.EXPLAIN}}
@dataclass(frozen=True,slots=True)
class DataView:
 dataset_id:str;dataset_manifest_hash:str;feature_order:tuple[str,...];rows:tuple[TrainingRow,...];role:SplitRole;fold_id:str;purpose:AccessPurpose
 @property
 def row_ids(self):return tuple(r.row_id for r in self.rows)
class GuardedDataset:
 def __init__(self,schema,rows):
  self.schema=schema;self._rows={r.row_id:r for r in rows};self._locked=False;self._audit=[];self._seq=0;self._test_reads=0
  if len(self._rows)!=schema.row_count:raise DataAccessError('row_count_mismatch','schema row count differs')
  if len(self._rows)!=len(rows):raise DataAccessError('duplicate_row_id','row IDs must be unique')
  width=len(schema.feature_order)
  for r in rows:
   if len(r.features)!=width:raise DataAccessError('feature_width_mismatch','row feature width differs',{'row_id':r.row_id})
   if len(r.target)!=schema.output_count:raise DataAccessError('target_width_mismatch','row target width differs',{'row_id':r.row_id})
   if r.event_time_ms>r.known_time_ms:raise DataAccessError('known_time_violation','row known time precedes event time',{'row_id':r.row_id})
   if not all(isfinite(float(x)) for x in r.features+r.target):raise DataAccessError('non_finite_row','row contains non-finite value',{'row_id':r.row_id})
 def lock_selection(self):self._locked=True
 @property
 def audit(self):return tuple(self._audit)
 def view(self,row_ids,role,purpose,phase,trainer_key,fold_id):
  ids=tuple(row_ids);self._seq+=1;allowed=purpose in _ALLOWED.get(role,set());reason='allowed'
  if role is SplitRole.FINAL_TEST and not self._locked:allowed=False;reason='final_test_is_sealed_until_selection_lock'
  if role is SplitRole.FINAL_TEST and self._test_reads>=1:allowed=False;reason='final_test_one_shot_already_consumed'
  if any(i not in self._rows for i in ids):allowed=False;reason='unknown_row_id'
  if len(set(ids))!=len(ids):allowed=False;reason='duplicate_requested_row_id'
  if any(i in self._rows and self._rows[i].role is not role for i in ids):allowed=False;reason='row_role_mismatch'
  self._audit.append(AccessAuditRecord(self._seq,canonical_sha256(ids),role,purpose,phase,trainer_key,allowed,reason))
  if not allowed:raise DataAccessError('dataset_access_denied',reason)
  if role is SplitRole.FINAL_TEST:self._test_reads+=1
  return DataView(self.schema.dataset_id,self.schema.dataset_manifest_hash,self.schema.feature_order,tuple(self._rows[i] for i in ids),role,fold_id,purpose)
