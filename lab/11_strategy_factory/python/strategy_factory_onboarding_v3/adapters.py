from __future__ import annotations
import copy
from dataclasses import dataclass
from typing import Any,Callable,Mapping
from .contracts import LegacyAdapterSpec,DifferentialObservation,DifferentialParityReport
from .canonical import stable_id
from .enums import ParityStatus
from .errors import OnboardingError
@dataclass(slots=True)
class LegacyAdapter:
    spec:LegacyAdapterSpec
    legacy_fn:Callable[[Mapping[str,Any]],Mapping[str,Any]]
    canonical_fn:Callable[[Mapping[str,Any]],Mapping[str,Any]]
    def observe(self,observation_id:str,known_time_ms:int,payload:Mapping[str,Any],tolerance:float=0.0)->DifferentialObservation:
        original=copy.deepcopy(dict(payload));left=self.legacy_fn(copy.deepcopy(original));right=self.canonical_fn(copy.deepcopy(original))
        if payload!=original:raise OnboardingError('input_mutated','adapter mutated caller input')
        keys=sorted(set(left)|set(right));deltas={}
        matched=True;reason='none'
        for key in keys:
            a,b=left.get(key),right.get(key)
            if isinstance(a,(int,float)) and isinstance(b,(int,float)):delta=abs(float(a)-float(b))
            else:delta=0.0 if a==b else max(1.0,tolerance+1.0)
            deltas[key]=delta
            if delta>tolerance:matched=False;reason='output_mismatch'
        return DifferentialObservation(observation_id,known_time_ms,left,right,deltas,matched,reason)

def measure_parity(spec:LegacyAdapterSpec,observations:tuple[DifferentialObservation,...],tolerance:float)->DifferentialParityReport:
    if not observations:return DifferentialParityReport(stable_id('parity-empty',spec.spec_hash),'1.0.0',spec.spec_hash,(),ParityStatus.INSUFFICIENT,0,0,0.0,tolerance,False)
    matched=sum(x.matched for x in observations);mismatch=len(observations)-matched;max_delta=max((max(x.field_deltas.values(),default=0.0) for x in observations),default=0.0)
    return DifferentialParityReport(stable_id('parity',{'adapter':spec.spec_hash,'obs':[x.observation_id for x in observations]}),'1.0.0',spec.spec_hash,observations,ParityStatus.PASS if mismatch==0 else ParityStatus.FAIL,matched,mismatch,max_delta,tolerance,False)
