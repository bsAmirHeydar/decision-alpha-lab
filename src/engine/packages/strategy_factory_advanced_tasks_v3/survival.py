from .contracts import *
from .canonical import stable_id,canonical_sha256
from .errors import CensoringError
from .math_utils import weighted_mean

class DiscreteHazardModel:
 def __init__(self,horizons_ms,alpha=1.0):self.horizons=tuple(sorted(set(int(x) for x in horizons_ms if x>0)));self.alpha=float(alpha);self.hazards=();self.causes={};self.state_hash=''
 def fit(self,observations):
  if not self.horizons:raise CensoringError('empty_horizons','survival horizons required')
  if any(o.duration_ms<0 or o.event not in (0,1) for o in observations):raise CensoringError('invalid_survival_observation','invalid duration or event')
  hz=[];causes=sorted({o.cause for o in observations if o.event and o.cause>0})
  cause_h={c:[] for c in causes};prev=0
  for h in self.horizons:
   at_risk=sum(o.weight for o in observations if o.duration_ms>=prev);events=sum(o.weight for o in observations if o.event and prev<o.duration_ms<=h);haz=(events+self.alpha)/(at_risk+2*self.alpha) if at_risk else 0.;hz.append(min(.999999,max(0.,haz)))
   for c in causes:
    ce=sum(o.weight for o in observations if o.event and o.cause==c and prev<o.duration_ms<=h);cause_h[c].append((ce+self.alpha)/(at_risk+len(causes)*self.alpha) if at_risk else 0.)
   prev=h
  self.hazards=tuple(hz);self.causes={c:tuple(v) for c,v in cause_h.items()};self.state_hash=canonical_sha256({'h':self.horizons,'hz':self.hazards,'causes':self.causes});return self
 def curve(self,row_id='global'):
  s=1.;surv=[];cum=[];ch=0.
  for hz in self.hazards:s*=1-hz;surv.append(max(0.,s));ch+=hz;cum.append(ch)
  h=canonical_sha256({'row':row_id,'state':self.state_hash});return SurvivalCurve(stable_id('ucesurvcurve',h),row_id,self.horizons,tuple(surv),tuple(cum),'uce.advanced.discrete_hazard@1.0.0',h)
 def competing_curve(self,row_id='global'):
  s=1.;cif={c:0. for c in self.causes};out={c:[] for c in self.causes};surv=[]
  for i,h in enumerate(self.horizons):
   for c in self.causes:cif[c]+=s*self.causes[c][i];out[c].append(min(1.,max(0.,cif[c])))
   s*=1-self.hazards[i];surv.append(max(0.,s))
  causes=tuple(sorted(out));matrix=tuple(tuple(out[c]) for c in causes);hh=canonical_sha256({'row':row_id,'state':self.state_hash,'matrix':matrix});return CompetingRiskCurve(stable_id('ucecif',hh),row_id,self.horizons,causes,matrix,tuple(surv),hh)

def survival_metrics(observations,risk_scores,curves,horizons_ms):
 comparable=correct=0
 for i,a in enumerate(observations):
  for j,b in enumerate(observations):
   if i>=j:continue
   if a.event and a.duration_ms<b.duration_ms:comparable+=1;correct+=risk_scores[a.row_id]>risk_scores[b.row_id]
   elif b.event and b.duration_ms<a.duration_ms:comparable+=1;correct+=risk_scores[b.row_id]>risk_scores[a.row_id]
 briers=[];cal=[]
 for k,h in enumerate(horizons_ms):
  vals=[];pred=[]
  for o in observations:
   if o.duration_ms<=h and not o.event:continue
   y=1.0 if o.duration_ms>h else 0.0;p=curves[o.row_id].survival[k];vals.append((y-p)**2);pred.append((y,p))
  if vals:briers.append(sum(vals)/len(vals));cal.append(abs(sum(y for y,_ in pred)/len(pred)-sum(p for _,p in pred)/len(pred)))
 ibs=sum(briers)/len(briers) if briers else 1.;ce=sum(cal)/len(cal) if cal else 1.;h=canonical_sha256({'obs':[(o.row_id,o.duration_ms,o.event) for o in observations],'risk':risk_scores,'ibs':ibs,'ce':ce})
 return SurvivalMetricReport(stable_id('ucesurvmetrics',h),correct/comparable if comparable else .5,ibs,ce,sum(o.event for o in observations),sum(1-o.event for o in observations),comparable,tuple(horizons_ms),h)
