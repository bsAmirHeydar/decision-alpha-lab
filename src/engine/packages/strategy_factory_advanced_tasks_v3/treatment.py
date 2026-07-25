from math import sqrt
from .contracts import *
from .canonical import stable_id,canonical_sha256
from .errors import SupportError
from .math_utils import fit_ridge,dot,mean,stdev

class DirectOutcomeSelector:
 def __init__(self,minimum_support=5,alpha=.01,uncertainty_penalty=0.0):self.minimum_support=minimum_support;self.alpha=alpha;self.uncertainty_penalty=uncertainty_penalty;self.models={};self.support={};self.residual_std={};self.state_hash=''
 def fit(self,rows,actions):
  for action in actions:
   subset=[r for r in rows if r.treatment_id==action]
   self.support[action]=len(subset)
   if len(subset)<self.minimum_support:continue
   coef,b=fit_ridge([r.features for r in subset],[r.target[0] for r in subset],[r.sample_weight for r in subset],self.alpha)
   residual=[r.target[0]-(b+dot(coef,r.features)) for r in subset];self.models[action]=(coef,b);self.residual_std[action]=stdev(residual)
  self.state_hash=canonical_sha256({'models':self.models,'support':self.support,'std':self.residual_std});return self
 def predict_one(self,row,mask,baseline_action=''):
  utilities={};uncertainties={}
  for action in mask.allowed_action_keys:
   if action not in self.models:continue
   coef,b=self.models[action];utilities[action]=b+dot(coef,row.features);uncertainties[action]=self.residual_std.get(action,0.)/sqrt(max(1,self.support.get(action,1)))
  if not utilities:
   h=canonical_sha256({'row':row.row_id,'mask':mask.evidence_hash,'decision':'abstain'});return TreatmentChoicePrediction(stable_id('ucetreatpred',h),row.row_id,mask.allowed_action_keys,{}, {},baseline_action,PolicyDecision.ABSTAIN,'no_supported_allowed_action',h)
  chosen=max(utilities,key=lambda a:(utilities[a]-self.uncertainty_penalty*uncertainties[a],a));h=canonical_sha256({'row':row.row_id,'u':utilities,'s':uncertainties,'chosen':chosen,'mask':mask.evidence_hash})
  return TreatmentChoicePrediction(stable_id('ucetreatpred',h),row.row_id,mask.allowed_action_keys,utilities,uncertainties,chosen,PolicyDecision.ACTION,'highest_supported_conservative_utility',h)

def audit_treatment_support(rows,declared_actions,minimum_count=5,minimum_propensity=.01):
 entries=[];blockers=[];warnings=[]
 for action in declared_actions:
  subset=[r for r in rows if r.treatment_id==action];count=len(subset);props=[max(minimum_propensity,float(getattr(r,'propensity',1.0))) for r in subset];ess=(sum(props)**2/sum(p*p for p in props)) if props and sum(p*p for p in props)>0 else 0.;minp=min(props) if props else 0.;maxp=max(props) if props else 0.
  if not subset:state=SupportState.UNSUPPORTED;reason='action_unobserved';blockers.append(f'unobserved:{action}')
  elif count<minimum_count:state=SupportState.WEAK;reason='below_minimum_count';warnings.append(f'weak:{action}')
  else:state=SupportState.SUPPORTED;reason='supported'
  entries.append(TreatmentSupportEntry(action,count,ess,minp,maxp,state,reason))
 h=canonical_sha256({'dataset':getattr(rows[0],'dataset_id','unknown') if rows else 'empty','entries':[e.__dict__ if hasattr(e,'__dict__') else (e.action_key,e.count,e.state.value) for e in entries]});return TreatmentSupportAudit(stable_id('ucetreatsupport',h),'unknown',tuple(entries),not blockers,not blockers,tuple(blockers),tuple(warnings),h)

def doubly_robust_value(logged_rows,policy_actions,q_hat,minimum_propensity=.01,support_audit_id=''):
 values=[];weights=[];clipped=0
 for row in logged_rows:
  p=max(minimum_propensity,row.propensity);clipped+=row.propensity<minimum_propensity;chosen=policy_actions[row.row_id];base=float(q_hat[(row.row_id,chosen)]);correction=(row.reward-base)/p if row.logged_action_key==chosen else 0.;values.append(base+correction);weights.append(1./p if row.logged_action_key==chosen else 0.)
 est=mean(values);se=stdev(values)/sqrt(max(1,len(values)));ess=(sum(weights)**2/sum(w*w for w in weights)) if sum(w*w for w in weights)>0 else 0.;h=canonical_sha256({'v':values,'p':policy_actions,'support':support_audit_id})
 return DoublyRobustReport(stable_id('ucedr',h),'candidate',len(values),est,se,ess,clipped,support_audit_id,h)
