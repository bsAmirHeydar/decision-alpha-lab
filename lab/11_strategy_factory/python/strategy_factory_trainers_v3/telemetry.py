from .contracts import TrainerTelemetry
from .canonical import stable_id
class TelemetrySink:
 def __init__(self):self.e=[];self.s=0
 def emit(self,phase,trainer,fold,code,severity,rows,features,elapsed=0,mem=0.,details=None):
  self.s+=1;self.e.append(TrainerTelemetry(stable_id('ucetel',{'s':self.s,'p':phase.value,'t':trainer,'f':fold,'c':code}),self.s,phase,trainer,fold,code,severity,elapsed,rows,features,mem,dict(details or {})))
 @property
 def events(self):return tuple(self.e)
