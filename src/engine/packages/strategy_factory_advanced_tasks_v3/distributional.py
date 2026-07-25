from .contracts import *
from .canonical import stable_id,canonical_sha256
from .math_utils import weighted_quantile,weighted_mean

class EmpiricalQuantileModel:
 def __init__(self,levels):
  self.levels=tuple(sorted(set(float(x) for x in levels)));self.values=();self.state_hash=''
  if not self.levels or self.levels[0]<=0 or self.levels[-1]>=1:raise ValueError('quantile levels must be inside (0,1)')
 def fit(self,values,weights=None):
  weights=weights or [1.]*len(values);self.values=tuple(weighted_quantile(values,weights,q) for q in self.levels);self.state_hash=canonical_sha256({'levels':self.levels,'values':self.values});return self
 def predict(self,row_id):
  h=canonical_sha256({'row':row_id,'state':self.state_hash});return QuantilePrediction(stable_id('ucequant',h),row_id,self.levels,self.values,all(a<=b for a,b in zip(self.values,self.values[1:])),h)

def fit_conformal_interval(calibration_y,calibration_center,alpha=.1,kind=IntervalKind.SYMMETRIC,groups=None):
 residuals=[abs(y-p) for y,p in zip(calibration_y,calibration_center)];q=weighted_quantile(residuals,[1.]*len(residuals),1-alpha)
 return {'alpha':alpha,'kind':kind,'radius':q,'size':len(residuals),'groups':tuple(groups or ()),'state_hash':canonical_sha256({'r':residuals,'a':alpha,'k':kind.value})}
def apply_conformal(row_id,center,state,group_key='global'):
 r=float(state['radius']);h=canonical_sha256({'row':row_id,'center':center,'state':state['state_hash'],'group':group_key});return ConformalInterval(stable_id('uceinterval',h),row_id,float(state['alpha']),center-r,center+r,state['kind'],int(state['size']),group_key,h)

def distributional_summary(row_id,samples,tail_level=.05,target_threshold=0.,stop_threshold=0.):
 s=sorted(float(x) for x in samples);n=len(s);expected=sum(s)/n if n else 0.;var=weighted_quantile(s,[1.]*n,tail_level) if n else 0.;tail=[x for x in s if x<=var];cvar=sum(tail)/len(tail) if tail else var;pp=sum(x>0 for x in s)/n if n else 0.;pt=sum(x>=target_threshold for x in s)/n if n else 0.;ps=sum(x<=stop_threshold for x in s)/n if n else 0.;h=canonical_sha256({'row':row_id,'s':s,'tail':tail_level,'tt':target_threshold,'st':stop_threshold});return DistributionalRiskSummary(stable_id('ucedist',h),row_id,expected,pp,var,cvar,pt,ps,tail_level,h)
def distributional_metrics(y,predictions,intervals):
 levels=predictions[0].levels if predictions else ();pin={}
 for j,q in enumerate(levels):pin[str(q)]=sum(max(q*(a-p.values[j]),(q-1)*(a-p.values[j])) for a,p in zip(y,predictions))/max(1,len(y))
 cov=sum(i.lower<=a<=i.upper for a,i in zip(y,intervals))/max(1,len(y));width=sum(i.upper-i.lower for i in intervals)/max(1,len(intervals));tail=abs(cov-(1-intervals[0].alpha)) if intervals else 1.;h=canonical_sha256({'pin':pin,'cov':cov,'width':width});return DistributionalMetricReport(stable_id('ucedistmetrics',h),pin,cov,width,tail,len(y),h)
