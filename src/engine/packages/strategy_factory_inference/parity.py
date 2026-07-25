from __future__ import annotations
from .models import ParityVector,ParityReport
from .enums import RuntimeBackend,ParityVerdict
from .hashing import stable_id

def evaluate_parity(manifest_hash: str, vectors, actual_raw, actual_calibrated, actual_classes,
                    *, backend=RuntimeBackend.PYTHON_REFERENCE, raw_tolerance=1e-6, calibrated_tolerance=1e-6):
    vectors=tuple(vectors); actual_raw=tuple(actual_raw); actual_calibrated=tuple(actual_calibrated); actual_classes=tuple(actual_classes)
    if not (len(vectors)==len(actual_raw)==len(actual_calibrated)==len(actual_classes)): raise ValueError("parity width mismatch")
    raw_errors=[abs(a-v.expected_raw_score) for a,v in zip(actual_raw,vectors)]
    cal_errors=[abs(a-v.expected_calibrated_score) for a,v in zip(actual_calibrated,vectors)]
    passed=[r<=raw_tolerance and c<=calibrated_tolerance and k==v.expected_class for r,c,k,v in zip(raw_errors,cal_errors,actual_classes,vectors)]
    rid=stable_id("parep",manifest_hash,int(backend),len(vectors),raw_tolerance,calibrated_tolerance)
    report=ParityReport(rid,manifest_hash,backend,len(vectors),sum(passed),len(vectors)-sum(passed),max(raw_errors,default=0.0),max(cal_errors,default=0.0),raw_tolerance,calibrated_tolerance,ParityVerdict.PASS if all(passed) else ParityVerdict.FAIL)
    return report.with_hash()
