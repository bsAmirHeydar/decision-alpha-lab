import json,math
from dataclasses import asdict
from strategy_factory_trainers_v3.interfaces import TrainerPlugin,FittedModel,CalibrationState,ExplanationArtifact
from strategy_factory_trainers_v3.contracts import TrainerCapabilityDescriptor,PredictionBatch,PredictionRecord
from strategy_factory_trainers_v3.enums import *
from strategy_factory_trainers_v3.canonical import canonical_json,canonical_sha256,stable_id
from strategy_factory_trainers_v3.prediction import make_batch
from .catalog import BY_ID
from .dependency import DependencyProbe
from .errors import DependencyUnavailableError,AlgorithmConfigurationError

def primitive(v):
 if hasattr(v,'tolist'):return primitive(v.tolist())
 if isinstance(v,dict):return {str(k):primitive(x) for k,x in sorted(v.items(),key=lambda z:str(z[0]))}
 if isinstance(v,(list,tuple)):return [primitive(x) for x in v]
 if isinstance(v,(str,bool,int,float)) or v is None:return v
 return str(v)
def sigmoid(x):
 if x>=0:return 1/(1+math.exp(-x))
 z=math.exp(x);return z/(1+z)
def estimator_factory(i,h,seed):
 if i=='linear_regression':
  from sklearn.linear_model import LinearRegression;return LinearRegression(**h)
 if i=='ridge_regression':
  from sklearn.linear_model import Ridge;return Ridge(random_state=seed,**h)
 if i=='lasso_regression':
  from sklearn.linear_model import Lasso;return Lasso(random_state=seed,**h)
 if i=='elastic_net':
  from sklearn.linear_model import ElasticNet;return ElasticNet(random_state=seed,**h)
 if i=='huber_regression':
  from sklearn.linear_model import HuberRegressor;return HuberRegressor(**h)
 if i=='logistic_regression':
  from sklearn.linear_model import LogisticRegression;return LogisticRegression(random_state=seed,**h)
 if i=='ridge_classifier':
  from sklearn.linear_model import RidgeClassifier;return RidgeClassifier(**h)
 if i=='linear_svm':
  from sklearn.svm import LinearSVC;return LinearSVC(random_state=seed,**h)
 if i=='rbf_svm':
  from sklearn.svm import SVC;return SVC(random_state=seed,**h)
 if i=='knn_classifier':
  from sklearn.neighbors import KNeighborsClassifier;return KNeighborsClassifier(**h)
 if i=='knn_regressor':
  from sklearn.neighbors import KNeighborsRegressor;return KNeighborsRegressor(**h)
 if i=='nearest_centroid':
  from sklearn.neighbors import NearestCentroid;return NearestCentroid(**h)
 if i=='decision_tree_classifier':
  from sklearn.tree import DecisionTreeClassifier;return DecisionTreeClassifier(random_state=seed,**h)
 if i=='decision_tree_regressor':
  from sklearn.tree import DecisionTreeRegressor;return DecisionTreeRegressor(random_state=seed,**h)
 if i=='random_forest_classifier':
  from sklearn.ensemble import RandomForestClassifier;return RandomForestClassifier(random_state=seed,**h)
 if i=='random_forest_regressor':
  from sklearn.ensemble import RandomForestRegressor;return RandomForestRegressor(random_state=seed,**h)
 if i=='extra_trees_classifier':
  from sklearn.ensemble import ExtraTreesClassifier;return ExtraTreesClassifier(random_state=seed,**h)
 if i=='extra_trees_regressor':
  from sklearn.ensemble import ExtraTreesRegressor;return ExtraTreesRegressor(random_state=seed,**h)
 if i=='gradient_boosting_classifier':
  from sklearn.ensemble import GradientBoostingClassifier;return GradientBoostingClassifier(random_state=seed,**h)
 if i=='gradient_boosting_regressor':
  from sklearn.ensemble import GradientBoostingRegressor;return GradientBoostingRegressor(random_state=seed,**h)
 if i=='hist_gradient_boosting_classifier':
  from sklearn.ensemble import HistGradientBoostingClassifier;return HistGradientBoostingClassifier(random_state=seed,**h)
 if i=='hist_gradient_boosting_regressor':
  from sklearn.ensemble import HistGradientBoostingRegressor;return HistGradientBoostingRegressor(random_state=seed,**h)
 if i=='gaussian_nb':
  from sklearn.naive_bayes import GaussianNB;return GaussianNB(**h)
 if i=='bernoulli_nb':
  from sklearn.naive_bayes import BernoulliNB;return BernoulliNB(**h)
 if i=='multinomial_nb':
  from sklearn.naive_bayes import MultinomialNB;return MultinomialNB(**h)
 if i in ('spline_logistic_gam','spline_ridge_gam'):
  from sklearn.pipeline import Pipeline
  from sklearn.preprocessing import SplineTransformer,StandardScaler
  n=h.pop('n_knots');deg=h.pop('degree')
  if i=='spline_logistic_gam':
   from sklearn.linear_model import LogisticRegression;model=LogisticRegression(random_state=seed,**h)
  else:
   from sklearn.linear_model import Ridge;model=Ridge(**h)
  return Pipeline([('spline',SplineTransformer(n_knots=n,degree=deg,include_bias=False)),('scale',StandardScaler()),('model',model)])
 if i=='xgboost_classifier':
  from xgboost import XGBClassifier;return XGBClassifier(random_state=seed,**h)
 if i=='xgboost_regressor':
  from xgboost import XGBRegressor;return XGBRegressor(random_state=seed,**h)
 if i=='lightgbm_classifier':
  from lightgbm import LGBMClassifier;return LGBMClassifier(random_state=seed,**h)
 if i=='lightgbm_regressor':
  from lightgbm import LGBMRegressor;return LGBMRegressor(random_state=seed,**h)
 if i=='catboost_classifier':
  from catboost import CatBoostClassifier;return CatBoostClassifier(random_seed=seed,**h)
 if i=='catboost_regressor':
  from catboost import CatBoostRegressor;return CatBoostRegressor(random_seed=seed,**h)
 raise AlgorithmConfigurationError('unknown_algorithm',i)
def snapshot_estimator(e,algorithm_id,params,train_predictions):
 target=e.named_steps['model'] if hasattr(e,'named_steps') and 'model' in e.named_steps else e;attrs={}
 for name in ('coef_','intercept_','classes_','feature_importances_','n_features_in_','n_iter_','class_prior_','theta_','var_','feature_log_prob_','class_log_prior_'):
  if hasattr(target,name):attrs[name]=primitive(getattr(target,name))
 if hasattr(target,'tree_'):
  t=target.tree_;attrs['tree_']={k:primitive(getattr(t,k)) for k in ('children_left','children_right','feature','threshold','value','impurity','n_node_samples')}
 return {'algorithm_id':algorithm_id,'estimator_module':type(e).__module__,'estimator_class':type(e).__name__,'parameters':primitive(params),'fitted_attributes':attrs,'train_prediction_fingerprint':canonical_sha256(primitive(train_predictions[:32])),'library':'scikit-compatible'}
class SklearnClassicalTrainer(TrainerPlugin):
 algorithm_id=''
 @classmethod
 def descriptor(cls):return BY_ID[cls.algorithm_id]
 @classmethod
 def capability(cls):
  d=cls.descriptor();tasks=tuple(TaskKind(x) for x in d.tasks);cal=(CalibrationKind.NONE,CalibrationKind.IDENTITY,CalibrationKind.PLATT,CalibrationKind.ISOTONIC) if d.probability_output else (CalibrationKind.NONE,CalibrationKind.IDENTITY)
  exports=tuple(ExportFormat(x) for x in d.export_formats if x in {z.value for z in ExportFormat})
  return TrainerCapabilityDescriptor(d.trainer_id,d.trainer_version,d.family.value,tasks,(ViewKind.TABULAR,),(TargetShape.SCALAR,TargetShape.CLASS_INDEX),supports_sample_weight=d.supports_sample_weight,missingness_support=MissingnessSupport.NATIVE if d.supports_missing_values else MissingnessSupport.PREIMPUTED,supports_multi_output=False,calibration_kinds=cal,explainability_kinds=(ExplainabilityKind.NONE,ExplainabilityKind.GLOBAL_IMPORTANCE,ExplainabilityKind.LOCAL_CONTRIBUTION,ExplainabilityKind.PARTIAL_DEPENDENCE),export_formats=exports,determinism=DeterminismLevel.NUMERIC_TOLERANCE,tags=d.tags)
 def configure(self,c,r):self.config=c;self.resources=r;self._models={}
 def validate(self,t,s):
  self.task=t;self.schema=s;a=DependencyProbe().evaluate(self.descriptor())
  if not a.available:raise DependencyUnavailableError('dependency_unavailable',a.reason,{'algorithm':self.algorithm_id,'statuses':[asdict(x) for x in a.dependencies]})
 def _xy(self,d):return [list(r.features) for r in d.rows],[r.target[0] for r in d.rows],[r.sample_weight for r in d.rows]
 def _raw_predict(self,e,X):
  if self.task.task_kind in (TaskKind.BINARY_CLASSIFICATION,TaskKind.MULTICLASS_CLASSIFICATION):
   if hasattr(e,'predict_proba'):
    q=e.predict_proba(X);return [float(row[-1]) if len(row)>1 else float(row[0]) for row in q]
   if hasattr(e,'decision_function'):
    q=e.decision_function(X);return [sigmoid(float(x[-1] if hasattr(x,'__len__') else x)) for x in q]
   return [float(x) for x in e.predict(X)]
  return [float(x) for x in e.predict(X)]
 def fit(self,d):
  X,y,w=self._xy(d);h=dict(self.descriptor().default_hyperparameters);h.update(dict(self.config.hyperparameters));e=estimator_factory(self.algorithm_id,h.copy(),self.config.seed)
  try:e.fit(X,y,sample_weight=w)
  except TypeError:e.fit(X,y)
  pred=self._raw_predict(e,X);s=snapshot_estimator(e,self.algorithm_id,h,pred);sh=canonical_sha256(s);self._models[sh]=e;return FittedModel(self.capability().key,self.task.key,d.feature_order,self.task.output_names,s,sh)
 def predict(self,m,d,l):
  if m.state_hash not in self._models:raise AlgorithmConfigurationError('model_runtime_state_unavailable','loaded research state requires governed library artifact rehydration')
  out=self._raw_predict(self._models[m.state_hash],[list(r.features) for r in d.rows]);kind=PredictionKind.PROBABILITY if self.task.task_kind in (TaskKind.BINARY_CLASSIFICATION,TaskKind.MULTICLASS_CLASSIFICATION) else PredictionKind.VALUE;return make_batch(d.rows,[(x,) for x in out],kind,l,m.output_names)
 def serialize(self,m):return canonical_json({'trainer_key':m.trainer_key,'task_key':m.task_key,'feature_order':m.feature_order,'output_names':m.output_names,'state':dict(m.state),'state_hash':m.state_hash})
 def load(self,p):
  o=json.loads(p)
  if canonical_sha256(o['state'])!=o['state_hash']:raise ValueError('state_hash_mismatch')
  return FittedModel(o['trainer_key'],o['task_key'],tuple(o['feature_order']),tuple(o['output_names']),o['state'],o['state_hash'])
 def calibrate(self,m,d,kind):
  if kind in (CalibrationKind.NONE,CalibrationKind.IDENTITY):return CalibrationState(CalibrationKind.IDENTITY,{},canonical_sha256({'kind':'identity','model':m.state_hash}))
  e=self._models[m.state_hash];scores=self._raw_predict(e,[list(r.features) for r in d.rows]);y=[float(r.target[0]) for r in d.rows]
  if kind is CalibrationKind.PLATT:
   a=1.0;b=0.0;lr=.05
   for _ in range(400):
    pa=[sigmoid(a*x+b) for x in scores];ga=sum((u-v)*x for u,v,x in zip(pa,y,scores))/len(y);gb=sum(u-v for u,v in zip(pa,y))/len(y);a-=lr*ga;b-=lr*gb
   params={'a':a,'b':b}
  elif kind is CalibrationKind.ISOTONIC:
   from sklearn.isotonic import IsotonicRegression
   iso=IsotonicRegression(out_of_bounds='clip').fit(scores,y);params={'x':primitive(iso.X_thresholds_),'y':primitive(iso.y_thresholds_)}
  else:raise AlgorithmConfigurationError('unsupported_calibration',kind.value)
  return CalibrationState(kind,params,canonical_sha256({'kind':kind.value,'params':params,'model':m.state_hash}))
 def apply_calibration(self,b,state):
  if state.kind is CalibrationKind.IDENTITY:return b
  def iso(x,xs,ys):
   if x<=xs[0]:return ys[0]
   if x>=xs[-1]:return ys[-1]
   for i in range(1,len(xs)):
    if x<=xs[i]:
     q=(x-xs[i-1])/(xs[i]-xs[i-1] or 1);return ys[i-1]+q*(ys[i]-ys[i-1])
  rec=[]
  for r in b.records:
   x=r.outputs[0];p=sigmoid(state.parameters['a']*x+state.parameters['b']) if state.kind is CalibrationKind.PLATT else iso(x,state.parameters['x'],state.parameters['y']);rec.append(PredictionRecord(r.prediction_id,r.row_id,(float(p),),r.prediction_kind,r.lineage,r.threshold,r.predicted_class))
  h=canonical_sha256([asdict(x) for x in rec]);return PredictionBatch(stable_id('ucecalbatch',h),tuple(rec),b.output_names,b.prediction_kind,True,h)
 def explain(self,m,d,kind):
  e=self._models[m.state_hash];target=e.named_steps['model'] if hasattr(e,'named_steps') and 'model' in e.named_steps else e;raw=getattr(target,'feature_importances_',None)
  if raw is None and hasattr(target,'coef_'):
   q=target.coef_;raw=q[0] if hasattr(q[0],'__len__') else q
  imp={n:abs(float(v)) for n,v in zip(d.feature_order,raw)} if raw is not None else {};return ExplanationArtifact(kind,imp,{},canonical_sha256({'model':m.state_hash,'rows':d.row_ids,'kind':kind.value,'imp':imp}))
 def dispose(self):self._models={}
def make_plugin_class(algorithm_id):return type('Trainer_'+algorithm_id,(SklearnClassicalTrainer,),{'algorithm_id':algorithm_id})
