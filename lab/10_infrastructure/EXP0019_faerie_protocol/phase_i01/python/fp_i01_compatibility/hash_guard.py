from __future__ import annotations
from pathlib import Path
from .canonical import aggregate_files_hash
from .models import DependencyPin, DependencyVerification
from .enums import CompatibilityStatus

def _files(repo:Path,pin:DependencyPin):
    base=repo/pin.relative_root; selected=set()
    for pattern in pin.file_globs:
        selected.update(p for p in base.glob(pattern) if p.is_file())
    return sorted(selected,key=lambda p:p.relative_to(repo).as_posix())

def verify_dependency(repo:Path,pin:DependencyPin)->DependencyVerification:
    files=_files(repo,pin)
    actual=aggregate_files_hash(repo,files) if files else ''
    if len(files)!=pin.expected_file_count:
        status=CompatibilityStatus.FAIL; reason='FILE_COUNT_MISMATCH'
    elif actual!=pin.expected_aggregate_sha256:
        status=CompatibilityStatus.FAIL; reason='AGGREGATE_HASH_MISMATCH'
    else:
        status=CompatibilityStatus.PASS; reason='EXACT_PIN_MATCH'
    return DependencyVerification(pin.dependency_id,pin.expected_file_count,len(files),pin.expected_aggregate_sha256,actual,status,reason)
