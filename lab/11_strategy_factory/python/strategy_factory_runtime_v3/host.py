from __future__ import annotations
import time
from typing import Callable,Mapping,Any
from .canonical import canonical_sha256,stable_id
from .contracts import *
from .bundle import validate_bundle
from .signing import require_valid_signature
from .preprocessing import transform
from .native_model import predict,decision
from .journal import DecisionJournal
from .enums import RuntimeMode,RuntimeDisposition
from .errors import ActivationError,RuntimeContractError
PolicyExecutor=Callable[[RuntimeRequest,str,Mapping[str,float]],tuple[RuntimeDisposition,str,tuple[str,...]]]

def default_policy_executor(request:RuntimeRequest,label:str,scores:Mapping[str,float]):
    if request.kill_switch:return RuntimeDisposition.REJECTED,'reject',('kill_switch',)
    return RuntimeDisposition.DECIDED,label,()
class BoundedRuntimeHost:
    def __init__(self,manifest:RuntimeBundleManifest,preprocessing:PreprocessingContract,model:NativeModelArtifact,export:ExportRecord,*,signature_secret:bytes,policy_executor:PolicyExecutor|None=None,journal:DecisionJournal|None=None,max_context_age_ms:int=60_000,max_latency_us:int=250_000,live_adapter_authorized:bool=False):
        validate_bundle(manifest,preprocessing,model,export);require_valid_signature(manifest,signature_secret)
        self.manifest=manifest;self.preprocessing=preprocessing;self.model=model;self.export=export;self.policy_executor=policy_executor or self._policy;self.journal=journal or DecisionJournal();self.max_context_age_ms=max_context_age_ms;self.max_latency_us=max_latency_us;self.live_adapter_authorized=live_adapter_authorized
    def _policy(self,request,label,scores):
        if request.kill_switch:return RuntimeDisposition.REJECTED,'reject',('kill_switch',)
        return RuntimeDisposition.DECIDED,label,()
    def decide(self,request:RuntimeRequest,completed_at_ms:int|None=None)->RuntimeDecision:
        prior=self.journal.get(request.request_id)
        if prior is not None:return prior
        if request.mode not in self.manifest.allowed_modes:raise ActivationError('mode_not_allowed','runtime mode not allowed by bundle')
        if request.mode is RuntimeMode.LIVE and not self.live_adapter_authorized:raise ActivationError('live_adapter_not_authorized','live mode requires isolated authorized adapter')
        if request.received_at_ms-request.known_time_ms>self.max_context_age_ms:raise RuntimeContractError('stale_context','context exceeds max age')
        t0=time.perf_counter_ns();x=transform(self.preprocessing,request.features);y=predict(self.model,x);label=decision(self.model,y);scores=dict(zip(self.model.output_names,y));disposition,label,reasons=self.policy_executor(request,label,scores);elapsed=(time.perf_counter_ns()-t0)//1000
        if elapsed>self.max_latency_us:disposition=RuntimeDisposition.FAILED;label='no_action';reasons=tuple(reasons)+('latency_breach',)
        now=completed_at_ms if completed_at_ms is not None else request.received_at_ms
        trace_hash=canonical_sha256({'request':request.request_id,'bundle':self.manifest.bundle_hash,'features':x,'scores':scores,'label':label,'reasons':reasons})
        d=RuntimeDecision(stable_id('runtime_decision',{'request':request.request_id,'bundle':self.manifest.bundle_hash}),request.request_id,request.occurrence_id,self.manifest.bundle_hash,self.manifest.generation,disposition,label,scores,request.known_time_ms,now,int(elapsed),tuple(reasons),False,trace_hash)
        return self.journal.append(d)
