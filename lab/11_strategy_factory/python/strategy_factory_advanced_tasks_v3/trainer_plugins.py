import json
from .canonical import canonical_json,canonical_sha256
from .ranking import PairwiseLinearRanker
from .treatment import DirectOutcomeSelector
from .survival import DiscreteHazardModel
from .distributional import EmpiricalQuantileModel
from .multitask import SharedLinearHeads
from .policy import ConservativePolicyImprovement
from strategy_factory_trainers_v3.interfaces import TrainerPlugin,FittedModel
from strategy_factory_trainers_v3.contracts import TrainerCapabilityDescriptor
from strategy_factory_trainers_v3.enums import *
from strategy_factory_trainers_v3.prediction import make_batch

class _Base(TrainerPlugin):
 def configure(self,c,r):self.config=c;self.resources=r
 def validate(self,t,s):self.task=t;self.schema=s
 def serialize(self,m):return canonical_json({'trainer_key':m.trainer_key,'task_key':m.task_key,'feature_order':m.feature_order,'output_names':m.output_names,'state':dict(m.state),'state_hash':m.state_hash})
 def load(self,payload):
  o=json.loads(payload)
  if canonical_sha256(o['state'])!=o['state_hash']:raise ValueError('state_hash_mismatch')
  return FittedModel(o['trainer_key'],o['task_key'],tuple(o['feature_order']),tuple(o['output_names']),o['state'],o['state_hash'])

class PairwiseRankerTrainer(_Base):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.advanced.pairwise_linear_ranker','1.0.0','advanced_ranking',(TaskKind.RANKING,),(ViewKind.TABULAR,),(TargetShape.LISTWISE,),supports_sample_weight=True,max_outputs=1,tags=('pairwise','group_aware'))
 def fit(self,d):
  m=PairwiseLinearRanker(**{k:v for k,v in self.config.hyperparameters.items() if k in ('epochs','learning_rate','l2','max_pairs_per_group')}).fit(d.rows,d.feature_order);s={'coefficients':m.coefficients,'state_hash':m.state_hash};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,canonical_sha256(s))
 def predict(self,m,d,l):return make_batch(d.rows,[(sum(a*b for a,b in zip(m.state['coefficients'],r.features)),) for r in d.rows],PredictionKind.RANK_SCORE,l,m.output_names)

class DirectOutcomeTreatmentTrainer(_Base):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.advanced.direct_outcome_selector','1.0.0','advanced_treatment',(TaskKind.TREATMENT_CHOICE,),(ViewKind.TABULAR,ViewKind.TREATMENT_MATRIX),(TargetShape.TREATMENT_UTILITY_VECTOR,TargetShape.SCALAR),supports_sample_weight=True,supports_multi_output=True,max_outputs=128,tags=('action_mask_required','support_audited'))
 def fit(self,d):
  actions=tuple(sorted({r.treatment_id for r in d.rows if r.treatment_id}));sel=DirectOutcomeSelector(int(self.config.hyperparameters.get('minimum_support',2)),float(self.config.hyperparameters.get('alpha',.01))).fit(d.rows,actions);state={'actions':actions,'models':sel.models,'support':sel.support,'residual_std':sel.residual_std};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,state,canonical_sha256(state))
 def predict(self,m,d,l):
  actions=tuple(m.state['actions']);outs=[]
  for r in d.rows:outs.append(tuple(float(m.state['models'][a][1])+sum(float(x)*y for x,y in zip(m.state['models'][a][0],r.features)) if a in m.state['models'] else -1e12 for a in actions))
  return make_batch(d.rows,outs,PredictionKind.TREATMENT_UTILITY,l,actions)

class DiscreteHazardTrainer(_Base):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.advanced.discrete_hazard','1.0.0','advanced_survival',(TaskKind.SURVIVAL,TaskKind.COMPETING_RISK),(ViewKind.TABULAR,ViewKind.PANEL),(TargetShape.DURATION_EVENT,TargetShape.DURATION_CAUSE),censoring_support=(CensoringSupport.RIGHT,CensoringSupport.COMPETING_RISK),supports_multi_output=True,max_outputs=256,tags=('censoring_aware','time_calibrated'))
 def fit(self,d):
  from .contracts import SurvivalObservation
  horizons=tuple(int(x) for x in self.config.hyperparameters.get('horizons_ms',(60000,300000,900000)));obs=[SurvivalObservation(r.row_id,r.censor_duration_ms,r.censor_event,int(r.target[0]) if self.task.task_kind is TaskKind.COMPETING_RISK else 0,r.sample_weight,r.known_time_ms) for r in d.rows];model=DiscreteHazardModel(horizons,float(self.config.hyperparameters.get('alpha',1.))).fit(obs);state={'horizons':model.horizons,'hazards':model.hazards,'causes':model.causes};return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,state,canonical_sha256(state))
 def predict(self,m,d,l):
  s=[];cur=1.
  for h in m.state['hazards']:cur*=1-float(h);s.append(cur)
  return make_batch(d.rows,[tuple(s) for _ in d.rows],PredictionKind.SURVIVAL_CURVE,l,tuple(f'survival_{x}' for x in m.state['horizons']))

class EmpiricalQuantileTrainer(_Base):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.advanced.empirical_quantiles','1.0.0','advanced_distributional',(TaskKind.QUANTILE,),(ViewKind.TABULAR,),(TargetShape.QUANTILE_VECTOR,TargetShape.SCALAR),supports_multi_output=True,max_outputs=64,calibration_kinds=(CalibrationKind.NONE,CalibrationKind.CONFORMAL),tags=('monotone_quantiles','tail_aware'))
 def fit(self,d):
  levels=tuple(float(x) for x in (self.task.quantile_levels or self.config.hyperparameters.get('levels',(.05,.25,.5,.75,.95))));q=EmpiricalQuantileModel(levels).fit([r.target[0] for r in d.rows],[r.sample_weight for r in d.rows]);state={'levels':q.levels,'values':q.values};return FittedModel(self.capability().key,self.task.key,d.feature_order,tuple(f'q_{x}' for x in q.levels),state,canonical_sha256(state))
 def predict(self,m,d,l):return make_batch(d.rows,[tuple(float(x) for x in m.state['values']) for _ in d.rows],PredictionKind.QUANTILES,l,tuple(f'q_{x}' for x in m.state['levels']))

class SharedLinearHeadsTrainer(_Base):
 @classmethod
 def capability(cls):return TrainerCapabilityDescriptor('uce.advanced.shared_linear_heads','1.0.0','advanced_multi_task',(TaskKind.MULTI_TASK,),(ViewKind.TABULAR,ViewKind.MULTI_VIEW),(TargetShape.VECTOR,),supports_multi_output=True,max_outputs=128,tags=('shared_features','weighted_heads'))
 def fit(self,d):
  keys=self.task.output_names;m=SharedLinearHeads(keys,self.config.hyperparameters.get('task_weights'),float(self.config.hyperparameters.get('alpha',.01))).fit(d.rows);state={'tasks':keys,'heads':m.heads,'weights':m.task_weights};return FittedModel(self.capability().key,self.task.key,d.feature_order,keys,state,canonical_sha256(state))
 def predict(self,m,d,l):
  outs=[]
  for r in d.rows:outs.append(tuple(float(m.state['heads'][k][1])+sum(float(x)*y for x,y in zip(m.state['heads'][k][0],r.features)) for k in m.state['tasks']))
  return make_batch(d.rows,outs,PredictionKind.VALUE,l,tuple(m.state['tasks']))

def register_advanced_trainers(registry):
 for cls in (PairwiseRankerTrainer,DirectOutcomeTreatmentTrainer,DiscreteHazardTrainer,EmpiricalQuantileTrainer,SharedLinearHeadsTrainer):registry.register(cls)
 return tuple(cls.capability().key for cls in (PairwiseRankerTrainer,DirectOutcomeTreatmentTrainer,DiscreteHazardTrainer,EmpiricalQuantileTrainer,SharedLinearHeadsTrainer))
