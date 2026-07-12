from .enums import TrainerLifecycleState
from .errors import LifecycleError
from .capabilities import CapabilityMatcher
_ALLOWED={TrainerLifecycleState.CREATED:{TrainerLifecycleState.CONFIGURED,TrainerLifecycleState.FAILED,TrainerLifecycleState.DISPOSED},TrainerLifecycleState.CONFIGURED:{TrainerLifecycleState.VALIDATED,TrainerLifecycleState.FAILED,TrainerLifecycleState.DISPOSED},TrainerLifecycleState.VALIDATED:{TrainerLifecycleState.FITTED,TrainerLifecycleState.FAILED,TrainerLifecycleState.DISPOSED},TrainerLifecycleState.FITTED:{TrainerLifecycleState.CALIBRATED,TrainerLifecycleState.EXPORTED,TrainerLifecycleState.FAILED,TrainerLifecycleState.DISPOSED},TrainerLifecycleState.CALIBRATED:{TrainerLifecycleState.EXPORTED,TrainerLifecycleState.FAILED,TrainerLifecycleState.DISPOSED},TrainerLifecycleState.EXPORTED:{TrainerLifecycleState.DISPOSED,TrainerLifecycleState.FAILED},TrainerLifecycleState.FAILED:{TrainerLifecycleState.DISPOSED},TrainerLifecycleState.DISPOSED:set()}
class TrainerSession:
 def __init__(self,p):self.plugin=p;self.state=TrainerLifecycleState.CREATED;self.model=None;self.calibration=None
 def move(self,n):
  if n not in _ALLOWED[self.state]:raise LifecycleError('illegal_lifecycle_transition',f'{self.state.value}->{n.value}')
  self.state=n
 def configure(self,c,r):self.plugin.configure(c,r);self.config=c;self.resources=r;self.move(TrainerLifecycleState.CONFIGURED)
 def validate(self,t,s):CapabilityMatcher.require(self.plugin.capability(),t,s,self.resources);self.plugin.validate(t,s);self.task=t;self.schema=s;self.move(TrainerLifecycleState.VALIDATED)
 def fit(self,d):self.model=self.plugin.fit(d);self.move(TrainerLifecycleState.FITTED);return self.model
 def predict(self,d,l):
  if self.state not in {TrainerLifecycleState.FITTED,TrainerLifecycleState.CALIBRATED,TrainerLifecycleState.EXPORTED}:raise LifecycleError('predict_before_fit','predict before fit')
  b=self.plugin.predict(self.model,d,l);return self.plugin.apply_calibration(b,self.calibration) if self.calibration else b
 def calibrate(self,d,k):self.calibration=self.plugin.calibrate(self.model,d,k);self.move(TrainerLifecycleState.CALIBRATED);return self.calibration
 def serialize(self):return self.plugin.serialize(self.model)
 def fail(self):
  if TrainerLifecycleState.FAILED in _ALLOWED[self.state]:self.move(TrainerLifecycleState.FAILED)
 def dispose(self):
  if self.state is not TrainerLifecycleState.DISPOSED:self.plugin.dispose();self.move(TrainerLifecycleState.DISPOSED)
