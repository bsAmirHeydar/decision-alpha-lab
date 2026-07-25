from __future__ import annotations
import platform,time
from dataclasses import asdict
from typing import Iterable
from .canonical import canonical_sha256,stable_id
from .contracts import *
from .preprocessing import transform
from .native_model import predict,decision
from .export import load_approved_native
from .mql5_mirror import preprocess_mirror,predict_mirror,decision_mirror

def _errors(a,b):
    abses=[abs(float(x)-float(y)) for x,y in zip(a,b)]
    rels=[abs(float(x)-float(y))/max(abs(float(x)),abs(float(y)),1e-12) for x,y in zip(a,b)]
    return max(abses,default=0.0),max(rels,default=0.0)
def certify_parity(manifest:RuntimeBundleManifest,preprocessing:PreprocessingContract,source_model:NativeModelArtifact,export_bytes:bytes,vectors:Iterable[ParityVector],tolerance:ParityTolerance=ParityTolerance(),created_at_ms:int|None=None)->ParityCertificate:
    exported=load_approved_native(export_bytes);obs=[];vectors=tuple(vectors)
    for v in vectors:
        sx=transform(preprocessing,v.features);sy=predict(source_model,sx);sd=decision(source_model,sy)
        ex=transform(preprocessing,v.features);ey=predict(exported,ex);ed=decision(exported,ey)
        mx=preprocess_mirror(preprocessing,v.features);my=predict_mirror(exported,mx);md=decision_mirror(exported,my)
        ae1,re1=_errors(sy,ey);ae2,re2=_errors(sy,my);ae=max(ae1,ae2);re=max(re1,re2)
        reasons=[]
        if ae>tolerance.absolute and re>tolerance.relative:reasons.append('numerical_tolerance_exceeded')
        if tolerance.decision_exact and len({sd,ed,md})!=1:reasons.append('decision_mismatch')
        if v.expected_decision is not None and sd!=v.expected_decision:reasons.append('expected_decision_mismatch')
        obs.append(ParityObservation(v.vector_id,tuple(sy),tuple(ey),tuple(my),sd,ed,md,ae,re,not reasons,tuple(reasons)))
    status=ParityStatus.PASS if obs and all(o.passed for o in obs) else ParityStatus.FAIL
    vector_hash=canonical_sha256([asdict(v) for v in vectors])
    return ParityCertificate(stable_id('parity_certificate',{'bundle':manifest.bundle_hash,'vectors':vector_hash}),'1.0.0',manifest.bundle_hash,vector_hash,status,tuple(obs),tolerance,platform.python_version(),'approved_native_v1','1.0.0',created_at_ms if created_at_ms is not None else int(time.time()*1000))
