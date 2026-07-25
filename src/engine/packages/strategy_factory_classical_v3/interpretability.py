from dataclasses import asdict
from math import sqrt
from strategy_factory_trainers_v3.canonical import canonical_sha256,stable_id
from strategy_factory_trainers_v3.contracts import TrainingRow
from strategy_factory_trainers_v3.data_access import DataView
from strategy_factory_trainers_v3.enums import SplitRole,ExplainabilityKind
from .contracts import *
from .errors import ExplanationLeakageError
class InterpretabilityEngine:
 @staticmethod
 def validate_request(q):
  if q.max_rows<1 or q.max_features<1:raise ValueError('invalid explanation budget')
  if q.role=='final_test' and q.for_selection:raise ExplanationLeakageError('hidden_test_selection_forbidden','final test explanations cannot select features or models')
  if q.scope is ExplanationScope.FINAL_TEST_AUDIT_ONLY and q.role!='final_test':raise ExplanationLeakageError('scope_role_mismatch','final-test audit scope requires final_test role')
 def native_importance(self,plugin,model,data,request,dataset_manifest_hash):
  self.validate_request(request);raw=plugin.explain(model,data,ExplainabilityKind.GLOBAL_IMPORTANCE);items=sorted(raw.global_importance.items(),key=lambda x:(-abs(x[1]),x[0]));records=tuple(FeatureImportanceRecord(n,data.feature_order.index(n),ImportanceKind.COEFFICIENT,float(v),0.0,1.0 if v>=0 else -1.0,data.fold_id,data.role.value,model.state_hash,i+1) for i,(n,v) in enumerate(items));h=canonical_sha256({'q':asdict(request),'records':[asdict(x) for x in records]});return ExplanationArtifact(stable_id('ucexplain',h),request.request_id,model.trainer_key,dataset_manifest_hash,data.fold_id,data.role.value,not(request.for_selection and data.role is SplitRole.FINAL_TEST),records,{}, {'compatible':True,'payload_required_later':True},('Importance is predictive, not causal.',),h)
 def permutation_importance(self,plugin,model,data,lineage,request,dataset_manifest_hash,metric):
  self.validate_request(request);base=plugin.predict(model,data,lineage);basev=metric(data.rows,base);records=[]
  for j,n in enumerate(data.feature_order[:request.max_features]):
   vals=[r.features[j] for r in data.rows];shift=max(1,len(vals)//3);perm=vals[shift:]+vals[:shift];rows=[]
   for r,v in zip(data.rows,perm):
    x=list(r.features);x[j]=v;rows.append(TrainingRow(r.row_id,tuple(x),r.target,r.role,r.fold_id,r.cluster_id,r.event_time_ms,r.known_time_ms,r.sample_weight,r.ranking_group,r.treatment_id,r.censor_event,r.censor_duration_ms))
   dv=DataView(data.dataset_id,data.dataset_manifest_hash,data.feature_order,tuple(rows),data.role,data.fold_id,data.purpose);pv=metric(rows,plugin.predict(model,dv,lineage));records.append(FeatureImportanceRecord(n,j,ImportanceKind.PERMUTATION,float(basev-pv),0.0,0.0,data.fold_id,data.role.value,model.state_hash,0))
  records.sort(key=lambda x:(-abs(x.mean_importance),x.feature_name));records=tuple(FeatureImportanceRecord(x.feature_name,x.feature_index,x.kind,x.mean_importance,x.std_importance,x.direction,x.fold_id,x.role,x.model_state_hash,i+1) for i,x in enumerate(records));h=canonical_sha256([asdict(x) for x in records]);return ExplanationArtifact(stable_id('ucexplain',h),request.request_id,model.trainer_key,dataset_manifest_hash,data.fold_id,data.role.value,True,records,{}, {'compatible':True},('Permutation importance depends on metric and feature dependence.',),h)
 @staticmethod
 def coefficient_stability(artifacts):
  by={}
  for a in artifacts:
   for r in a.records:by.setdefault(r.feature_name,[]).append(r.mean_importance)
  out={}
  for n,v in by.items():
   m=sum(v)/len(v);sd=sqrt(sum((x-m)**2 for x in v)/max(1,len(v)-1));out[n]={'mean':m,'std':sd,'sign_consistency':sum(1 for x in v if x*m>=0)/len(v)}
  return out
