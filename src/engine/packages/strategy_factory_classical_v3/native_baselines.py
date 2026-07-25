import json,random
from strategy_factory_trainers_v3.interfaces import TrainerPlugin,FittedModel,CalibrationState
from strategy_factory_trainers_v3.contracts import TrainerCapabilityDescriptor
from strategy_factory_trainers_v3.enums import *
from strategy_factory_trainers_v3.canonical import canonical_json,canonical_sha256
from strategy_factory_trainers_v3.prediction import make_batch
from .catalog import BY_ID
from .errors import AlgorithmConfigurationError
class _Base(TrainerPlugin):
 algorithm_id=''
 @classmethod
 def descriptor(cls):return BY_ID[cls.algorithm_id]
 @classmethod
 def capability(cls):
  d=cls.descriptor();return TrainerCapabilityDescriptor(d.trainer_id,d.trainer_version,d.family.value,tuple(TaskKind(x) for x in d.tasks),(ViewKind.TABULAR,),(TargetShape.SCALAR,),supports_sample_weight=True,calibration_kinds=(CalibrationKind.NONE,CalibrationKind.IDENTITY),explainability_kinds=(ExplainabilityKind.NONE,ExplainabilityKind.GLOBAL_IMPORTANCE),export_formats=(ExportFormat.NATIVE_JSON,),tags=d.tags)
 def configure(self,c,r):self.config=c;self.resources=r
 def validate(self,t,s):self.task=t;self.schema=s
 def serialize(self,m):return canonical_json({'trainer_key':m.trainer_key,'task_key':m.task_key,'feature_order':m.feature_order,'output_names':m.output_names,'state':dict(m.state),'state_hash':m.state_hash})
 def load(self,p):
  o=json.loads(p)
  if canonical_sha256(o['state'])!=o['state_hash']:raise ValueError('state_hash_mismatch')
  return FittedModel(o['trainer_key'],o['task_key'],tuple(o['feature_order']),tuple(o['output_names']),o['state'],o['state_hash'])
 def calibrate(self,m,d,k):return CalibrationState(CalibrationKind.IDENTITY,{},canonical_sha256({'kind':'identity','model':m.state_hash}))
 def dispose(self):pass
class ConstantTrainer(_Base):
 constant=0.0
 def fit(self,d):
  s={'algorithm_id':self.algorithm_id,'constant':float(self.constant),'row_count':len(d.rows)};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):return make_batch(d.rows,[(float(m.state['constant']),) for _ in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class NeverTradeTrainer(ConstantTrainer):algorithm_id='never_trade';constant=0.0
class AlwaysTradeTrainer(ConstantTrainer):algorithm_id='always_trade';constant=1.0
class PrevalenceTrainer(_Base):
 algorithm_id='prevalence'
 def fit(self,d):
  sw=sum(r.sample_weight for r in d.rows);q=sum(r.target[0]*r.sample_weight for r in d.rows)/sw;s={'algorithm_id':self.algorithm_id,'prior':q,'row_count':len(d.rows)};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):return make_batch(d.rows,[(float(m.state['prior']),) for _ in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class ManualThresholdTrainer(_Base):
 algorithm_id='manual_threshold'
 def fit(self,d):
  h=dict(self.descriptor().default_hyperparameters);h.update(dict(self.config.hyperparameters));i=int(h['feature_index']);t=float(h['threshold']);q=1 if int(h.get('direction',1))>=0 else -1
  if i<0 or i>=len(d.feature_order):raise AlgorithmConfigurationError('feature_index_out_of_range','manual feature index invalid')
  s={'algorithm_id':self.algorithm_id,'feature_index':i,'threshold':t,'direction':q,'feature_name':d.feature_order[i]};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):
  i=int(m.state['feature_index']);t=float(m.state['threshold']);q=int(m.state['direction']);return make_batch(d.rows,[(1.0 if q*(r.features[i]-t)>=0 else 0.0,) for r in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class SingleFeatureSearchTrainer(_Base):
 algorithm_id='single_feature_search'
 def fit(self,d):
  best=None
  for j in range(len(d.feature_order)):
   vals=sorted(set(float(r.features[j]) for r in d.rows));cuts=[vals[0]-1e-12]+[(a+b)/2 for a,b in zip(vals,vals[1:])]+[vals[-1]+1e-12]
   for q in (-1,1):
    for t in cuts:
     score=sum(r.sample_weight*(int(q*(r.features[j]-t)>=0)==int(r.target[0]>=.5)) for r in d.rows)/sum(r.sample_weight for r in d.rows);key=(score,-j,-abs(t),q)
     if best is None or key>best[0]:best=(key,j,t,q)
  _,j,t,q=best;s={'algorithm_id':self.algorithm_id,'feature_index':j,'threshold':t,'direction':q,'feature_name':d.feature_order[j],'train_accuracy':best[0][0]};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):
  j=int(m.state['feature_index']);t=float(m.state['threshold']);q=int(m.state['direction']);return make_batch(d.rows,[(1.0 if q*(r.features[j]-t)>=0 else 0.0,) for r in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class RateMatchedNullTrainer(PrevalenceTrainer):
 algorithm_id='rate_matched_null'
 def predict(self,m,d,l):
  p=float(m.state['prior']);return make_batch(d.rows,[(1.0 if random.Random(f'{self.config.seed}:{r.row_id}').random()<p else 0.0,) for r in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class RandomNullTrainer(PrevalenceTrainer):
 algorithm_id='random_null'
 def predict(self,m,d,l):return make_batch(d.rows,[(random.Random(f'{self.config.seed}:{r.row_id}').random(),) for r in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
NATIVE_BASELINES=(NeverTradeTrainer,AlwaysTradeTrainer,PrevalenceTrainer,ManualThresholdTrainer,SingleFeatureSearchTrainer,RateMatchedNullTrainer,RandomNullTrainer)
