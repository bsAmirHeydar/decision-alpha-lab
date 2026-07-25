from .contracts import *
from .canonical import stable_id,canonical_sha256
from .math_utils import fit_ridge,dot,mean

class SharedLinearHeads:
 def __init__(self,task_keys,task_weights=None,alpha=.01):self.task_keys=tuple(task_keys);self.task_weights=tuple(task_weights or [1.]*len(task_keys));self.alpha=alpha;self.heads={};self.state_hash=''
 def fit(self,rows):
  x=[r.features for r in rows];weights=[r.sample_weight for r in rows]
  for j,key in enumerate(self.task_keys):self.heads[key]=fit_ridge(x,[r.target[j] for r in rows],weights,self.alpha)
  self.state_hash=canonical_sha256({'tasks':self.task_keys,'weights':self.task_weights,'heads':self.heads});return self
 def predict(self,row):return {k:b+dot(c,row.features) for k,(c,b) in self.heads.items()}
 def report(self,rows):
  heads=[]
  for j,key in enumerate(self.task_keys):
   pred=[self.predict(r)[key] for r in rows];loss=sum((r.target[j]-p)**2*r.sample_weight for r,p in zip(rows,pred))/max(1e-12,sum(r.sample_weight for r in rows));heads.append(MultiTaskHeadResult(key,loss,self.task_weights[j],canonical_sha256(pred)))
  weighted=sum(h.loss*h.weight for h in heads)/max(1e-12,sum(h.weight for h in heads));losses=[h.loss for h in heads];balance=1/(1+(max(losses)-min(losses))) if losses else 1.;h=canonical_sha256({'heads':heads,'state':self.state_hash});return MultiTaskLossReport(stable_id('ucemultitask',h),tuple(heads),weighted,balance,self.state_hash,h)

class RegimeGate:
 def __init__(self,minimum_support=10,fallback=RegimeFallback.GLOBAL):self.minimum_support=minimum_support;self.fallback=fallback;self.centroids={};self.support={};self.experts={};self.global_expert='';self.state_hash=''
 def fit(self,rows,regime_by_row,expert_by_regime,global_expert):
  self.global_expert=global_expert;self.experts=dict(expert_by_regime)
  for regime in sorted(set(regime_by_row.values())):
   subset=[r for r in rows if regime_by_row[r.row_id]==regime];self.support[regime]=len(subset)
   if subset:self.centroids[regime]=tuple(sum(r.features[j] for r in subset)/len(subset) for j in range(len(subset[0].features)))
  self.state_hash=canonical_sha256({'centroids':self.centroids,'support':self.support,'experts':self.experts,'global':global_expert});return self
 def assign(self,row):
  if not self.centroids:
   h=canonical_sha256({'row':row.row_id,'state':self.state_hash,'empty':True});return RegimeAssignment(stable_id('uceregime',h),row.row_id,'global',1.,0,True,'no_regime_centroids',h)
  distances={k:sum((a-b)**2 for a,b in zip(row.features,c)) for k,c in self.centroids.items()};regime=min(distances,key=lambda k:(distances[k],k));support=self.support[regime];fallback=support<self.minimum_support;reason='sparse_regime' if fallback else 'supported_regime';h=canonical_sha256({'row':row.row_id,'regime':regime,'support':support,'state':self.state_hash});return RegimeAssignment(stable_id('uceregime',h),row.row_id,regime,1/(1+distances[regime]),support,fallback,reason,h)
 def select(self,row):
  a=self.assign(row);expert=self.global_expert if a.fallback_used else self.experts.get(a.regime_id,self.global_expert);decision=GateDecision.WARN if a.fallback_used else GateDecision.ACCEPT;h=canonical_sha256({'assignment':a.evidence_hash,'expert':expert});return ExpertGateResult(stable_id('ucegate',h),row.row_id,expert,a.fallback_used,a.regime_id,a.support_count,decision,a.fallback_reason,h)
