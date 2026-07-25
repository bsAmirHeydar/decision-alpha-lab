from math import sqrt
from .contracts import *
from .canonical import stable_id,canonical_sha256
from .errors import PolicyError
from .math_utils import mean,stdev,normal_lcb

def audit_policy_support(rows,declared_actions,minimum_action_count=5,minimum_propensity=.01):
 observed=sorted({r.logged_action_key for r in rows});unseen=sorted(set(declared_actions)-set(observed));masked=sum(r.logged_action_key not in r.allowed_action_keys for r in rows);counts={a:sum(r.logged_action_key==a for r in rows) for a in declared_actions};blockers=[]
 if unseen:blockers.append('unseen_actions:'+','.join(unseen))
 if masked:blockers.append(f'logged_action_mask_violations:{masked}')
 if any(c<minimum_action_count for c in counts.values()):blockers.append('insufficient_action_support')
 minp=min((r.propensity for r in rows),default=0.)
 if minp<minimum_propensity:blockers.append('propensity_below_floor')
 decision=GateDecision.REJECT if blockers else GateDecision.ACCEPT;h=canonical_sha256({'declared':declared_actions,'observed':observed,'counts':counts,'masked':masked,'minp':minp});return PolicySupportAudit(stable_id('ucepolicysupport',h),tuple(declared_actions),tuple(observed),tuple(unseen),masked,min(counts.values()) if counts else 0,minp,decision,tuple(blockers),h)

class ConservativePolicyImprovement:
 def __init__(self,action_keys,minimum_support=5,uncertainty_z=1.96,minimum_improvement=0.0):self.action_keys=tuple(action_keys);self.minimum_support=minimum_support;self.uncertainty_z=uncertainty_z;self.minimum_improvement=minimum_improvement;self.stats={};self.state_hash=''
 def fit(self,rows):
  for action in self.action_keys:
   vals=[r.reward for r in rows if r.logged_action_key==action];self.stats[action]=(mean(vals),stdev(vals),len(vals))
  self.state_hash=canonical_sha256({'actions':self.action_keys,'stats':self.stats,'z':self.uncertainty_z,'min':self.minimum_improvement});return self
 def decide(self,row,baseline_action):
  allowed=set(row.allowed_action_keys);scores=[]
  for action in self.action_keys:
   m,s,n=self.stats.get(action,(0.,0.,0.));state=SupportState.MASKED if action not in allowed else (SupportState.UNSUPPORTED if n==0 else SupportState.WEAK if n<self.minimum_support else SupportState.SUPPORTED);se=s/sqrt(max(1,n));scores.append(PolicyActionScore(action,m,se,normal_lcb(m,se,self.uncertainty_z),n,state))
  eligible=[x for x in scores if x.support_state is SupportState.SUPPORTED]
  base=next((x for x in scores if x.action_key==baseline_action),None)
  if not eligible or base is None:
   selected=baseline_action;decision=PolicyDecision.ABSTAIN;improvement=0.;reason='no_supported_improvement_candidate'
  else:
   best=max(eligible,key=lambda x:(x.conservative_value,x.action_key));improvement=best.conservative_value-base.mean_utility
   if improvement>=self.minimum_improvement:selected=best.action_key;decision=PolicyDecision.ACTION;reason='conservative_improvement_passed'
   else:selected=baseline_action;decision=PolicyDecision.BASELINE;reason='improvement_lower_bound_failed'
  h=canonical_sha256({'row':row.row_id,'scores':scores,'selected':selected,'baseline':baseline_action,'reason':reason});return ConservativePolicyDecision(stable_id('ucepolicydecision',h),row.row_id,tuple(scores),selected,baseline_action,decision,improvement,reason,h)

def compare_logged_policy(rows,candidate_actions,baseline_actions,q_hat,support_audit_id='',z=1.96,propensity_floor=.01):
 def dr(actions):
  values=[];weights=[]
  for r in rows:
   a=actions[r.row_id];q=float(q_hat[(r.row_id,a)]);p=max(propensity_floor,r.propensity);values.append(q+((r.reward-q)/p if r.logged_action_key==a else 0.));weights.append(1./p if r.logged_action_key==a else 0.)
  return mean(values),stdev(values)/sqrt(max(1,len(values))),((sum(weights)**2/sum(w*w for w in weights)) if sum(w*w for w in weights)>0 else 0.)
 cv,cse,ess=dr(candidate_actions);bv,bse,_=dr(baseline_actions);imp=cv-bv;se=sqrt(cse*cse+bse*bse);lcb=imp-z*se;decision=GateDecision.ACCEPT if lcb>0 else GateDecision.REJECT;h=canonical_sha256({'cv':cv,'bv':bv,'se':se,'support':support_audit_id});return LoggedPolicyComparison(stable_id('ucepolicycmp',h),'candidate','baseline',cv,bv,imp,se,lcb,ess,support_audit_id,decision,h)
