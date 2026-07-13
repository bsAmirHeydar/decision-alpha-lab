from __future__ import annotations
import threading,time
from dataclasses import replace
from .canonical import stable_id
from .contracts import *
from .enums import GenerationState,ParityStatus
from .errors import ActivationError
class GenerationManager:
    def __init__(self,genesis_hash:str='0'*64):
        self._lock=threading.RLock();self._records={};self._active_hash=genesis_hash;self._genesis=genesis_hash;self._receipts={}
    @property
    def active_hash(self):
        with self._lock:return self._active_hash
    def build(self,manifest:RuntimeBundleManifest)->GenerationRecord:
        with self._lock:
            rec=GenerationRecord(manifest.bundle_hash,manifest.generation,GenerationState.BUILT,self._active_hash);self._records[manifest.bundle_hash]=rec;return rec
    def warm(self,bundle_hash:str)->GenerationRecord:
        with self._lock:
            rec=self._require(bundle_hash,GenerationState.BUILT);rec=replace(rec,state=GenerationState.WARMED);self._records[bundle_hash]=rec;return rec
    def validate(self,bundle_hash:str,certificate:ParityCertificate)->GenerationRecord:
        with self._lock:
            rec=self._require(bundle_hash,GenerationState.WARMED)
            if certificate.bundle_hash!=bundle_hash or certificate.status is not ParityStatus.PASS:raise ActivationError('parity_failure','generation cannot validate without PASS parity certificate')
            rec=replace(rec,state=GenerationState.VALIDATED,parity_certificate_hash=certificate.certificate_hash);self._records[bundle_hash]=rec;return rec
    def activate(self,bundle_hash:str,idempotency_key:str,at_ms:int|None=None)->ActivationReceipt:
        with self._lock:
            if idempotency_key in self._receipts:return self._receipts[idempotency_key]
            rec=self._require(bundle_hash,GenerationState.VALIDATED);now=at_ms if at_ms is not None else int(time.time()*1000);previous=self._active_hash
            if previous in self._records and self._records[previous].state is GenerationState.ACTIVE:self._records[previous]=replace(self._records[previous],state=GenerationState.RETIRED,retired_at_ms=now)
            rec=replace(rec,state=GenerationState.ACTIVE,activated_at_ms=now);self._records[bundle_hash]=rec;self._active_hash=bundle_hash
            receipt=ActivationReceipt(stable_id('activation',{'bundle':bundle_hash,'key':idempotency_key}),bundle_hash,rec.generation,previous,now,idempotency_key,GenerationState.ACTIVE);self._receipts[idempotency_key]=receipt;return receipt
    def rollback(self,target_hash:str,idempotency_key:str,at_ms:int|None=None)->ActivationReceipt:
        with self._lock:
            if target_hash not in self._records:raise ActivationError('unknown_rollback_target','rollback target not registered')
            target=self._records[target_hash]
            if target.state not in (GenerationState.RETIRED,GenerationState.VALIDATED,GenerationState.ACTIVE):raise ActivationError('invalid_rollback_target','rollback target not activatable')
            if target.state is GenerationState.RETIRED:self._records[target_hash]=replace(target,state=GenerationState.VALIDATED,retired_at_ms=None)
            return self.activate(target_hash,idempotency_key,at_ms)
    def quarantine(self,bundle_hash:str,reason:str):
        with self._lock:
            rec=self._records[bundle_hash];self._records[bundle_hash]=replace(rec,state=GenerationState.QUARANTINED,failure_reasons=rec.failure_reasons+(reason,))
            if self._active_hash==bundle_hash:self._active_hash=rec.previous_bundle_hash
            return self._records[bundle_hash]
    def record(self,bundle_hash):return self._records[bundle_hash]
    def _require(self,bundle_hash,state):
        if bundle_hash not in self._records:raise ActivationError('unknown_generation','generation not built')
        rec=self._records[bundle_hash]
        if rec.state is not state:raise ActivationError('invalid_generation_transition',f'expected {state.value}, got {rec.state.value}')
        return rec
