import json
from math import sqrt
from .canonical import canonical_json,canonical_sha256
from .contracts import *
from .enums import *
from .interfaces import TrainerPlugin,FittedModel
from .prediction import make_batch
from .errors import SerializationError
class Base:
 def configure(self,c,r):self.config=c;self.resources=r
 def validate(self,t,s):self.task=t;self.schema=s
 def serialize(self,m):return canonical_json({'trainer_key':m.trainer_key,'task_key':m.task_key,'feature_order':m.feature_order,'output_names':m.output_names,'state':dict(m.state),'state_hash':m.state_hash})
 def load(self,p):
  try:o=json.loads(p)
  except Exception as e:raise SerializationError('invalid_model_payload','invalid json') from e
  if canonical_sha256(o['state'])!=o['state_hash']:raise SerializationError('state_hash_mismatch','corrupt model')
  return FittedModel(o['trainer_key'],o['task_key'],tuple(o['feature_order']),tuple(o['output_names']),o['state'],o['state_hash'])
class PriorBinaryTrainer(Base,TrainerPlugin):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.reference.prior_binary','1.0.0','reference_probability',(TaskKind.BINARY_CLASSIFICATION,),(ViewKind.TABULAR,),(TargetShape.SCALAR,),calibration_kinds=(CalibrationKind.NONE,CalibrationKind.IDENTITY),explainability_kinds=(ExplainabilityKind.NONE,ExplainabilityKind.GLOBAL_IMPORTANCE),tags=('conformance','baseline'))
 def fit(self,d):
  p=sum(r.target[0]*r.sample_weight for r in d.rows)/sum(r.sample_weight for r in d.rows);s={'prior':p,'row_count':len(d.rows)}
  return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):return make_batch(d.rows,[(float(m.state['prior']),) for _ in d.rows],PredictionKind.PROBABILITY,l,m.output_names)
class MeanRegressionTrainer(Base,TrainerPlugin):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.reference.mean_regression','1.0.0','reference_regression',(TaskKind.REGRESSION,),(ViewKind.TABULAR,),(TargetShape.SCALAR,),tags=('conformance','baseline'))
 def fit(self,d):
  p=sum(r.target[0]*r.sample_weight for r in d.rows)/sum(r.sample_weight for r in d.rows);s={'mean':p,'row_count':len(d.rows)}
  return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):return make_batch(d.rows,[(float(m.state['mean']),) for _ in d.rows],PredictionKind.VALUE,l,m.output_names)
class LinearRankingTrainer(Base,TrainerPlugin):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.reference.linear_ranker','1.0.0','reference_ranking',(TaskKind.RANKING,),(ViewKind.TABULAR,),(TargetShape.LISTWISE,),explainability_kinds=(ExplainabilityKind.NONE,ExplainabilityKind.GLOBAL_IMPORTANCE,ExplainabilityKind.LOCAL_CONTRIBUTION),tags=('conformance','baseline'))
 def fit(self,d):
  sw=sum(r.sample_weight for r in d.rows);my=sum(r.target[0]*r.sample_weight for r in d.rows)/sw;coef=[]
  for j in range(len(d.feature_order)):
   mx=sum(r.features[j]*r.sample_weight for r in d.rows)/sw;cov=sum(r.sample_weight*(r.features[j]-mx)*(r.target[0]-my) for r in d.rows);var=sum(r.sample_weight*(r.features[j]-mx)**2 for r in d.rows);coef.append(cov/var if var else 0.)
  n=sqrt(sum(x*x for x in coef)) or 1.;coef=[x/n for x in coef];s={'coefficients':coef,'intercept':my,'row_count':len(d.rows)}
  return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):
  c=[float(x) for x in m.state['coefficients']];return make_batch(d.rows,[(float(m.state['intercept'])+sum(a*b for a,b in zip(r.features,c)),) for r in d.rows],PredictionKind.RANK_SCORE,l,m.output_names)
def register_reference_trainers(r):r.register(PriorBinaryTrainer);r.register(MeanRegressionTrainer);r.register(LinearRankingTrainer)
