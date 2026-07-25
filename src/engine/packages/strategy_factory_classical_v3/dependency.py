from importlib import import_module
from importlib.metadata import version,PackageNotFoundError
from dataclasses import asdict
from .contracts import *
from .enums import *
from strategy_factory_trainers_v3.canonical import canonical_sha256
class DependencyProbe:
 def __init__(self,disabled=()):self.disabled=set(disabled)
 def probe_one(self,r):
  if r.module in self.disabled:return DependencyStatus(r.module,AvailabilityState.DISABLED,'','explicitly disabled',canonical_sha256({'module':r.module,'state':'disabled'}))
  try:
   import_module(r.module)
   try:v=version(r.distribution)
   except PackageNotFoundError:v='unknown'
   return DependencyStatus(r.module,AvailabilityState.AVAILABLE,v,'',canonical_sha256({'module':r.module,'version':v}))
  except Exception as e:return DependencyStatus(r.module,AvailabilityState.UNAVAILABLE,'',f'{type(e).__name__}: {e}',canonical_sha256({'module':r.module,'error':type(e).__name__}))
 def evaluate(self,d):
  s=tuple(self.probe_one(x) for x in d.dependencies);blocking=[x for x,r in zip(s,d.dependencies) if r.mode is DependencyMode.REQUIRED and x.state is not AvailabilityState.AVAILABLE];ok=not blocking and not(d.dependencies and all(x.state is not AvailabilityState.AVAILABLE for x in s));reason='available' if ok else('required dependency unavailable' if blocking else 'algorithm dependency unavailable');return AlgorithmAvailability(d.key,ok,s,reason,canonical_sha256({'d':d.descriptor_hash,'s':[asdict(x) for x in s],'ok':ok}))
