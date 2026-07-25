from dataclasses import dataclass,field
@dataclass(slots=True)
class AtomTelemetry:
 invocations:int=0; rejections:int=0; by_kind:dict[str,int]=field(default_factory=dict); by_error:dict[str,int]=field(default_factory=dict)
 def accepted(self,kind:str): self.invocations+=1; self.by_kind[kind]=self.by_kind.get(kind,0)+1
 def rejected(self,code:str): self.rejections+=1; self.by_error[code]=self.by_error.get(code,0)+1
 def snapshot(self): return {'invocations':self.invocations,'rejections':self.rejections,'by_kind':dict(sorted(self.by_kind.items())),'by_error':dict(sorted(self.by_error.items()))}
