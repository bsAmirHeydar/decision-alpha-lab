from __future__ import annotations
from pathlib import Path
from .canonical import bytes_sha256,canonical_sha256,stable_id,safe_relative_path
from .contracts import CoreSnapshot,EngineInvarianceReport
from .enums import InvarianceStatus
CORE_PREFIXES=('src/engine/packages/strategy_factory_contracts_v3','src/engine/packages/strategy_factory_economics_v3','src/engine/packages/strategy_factory_experiments_v3','src/engine/packages/strategy_factory_promotion_v3','src/engine/packages/strategy_factory_policy_v3','src/engine/packages/strategy_factory_runtime_v3')
def snapshot(root:Path,captured_at_ms:int=0)->CoreSnapshot:
    hashes={}
    for prefix in CORE_PREFIXES:
        base=root/prefix
        if not base.exists():continue
        for p in sorted(x for x in base.rglob('*') if x.is_file() and '__pycache__' not in x.parts):
            rel=p.relative_to(root).as_posix();hashes[rel]=bytes_sha256(p.read_bytes())
    root_hash=canonical_sha256(hashes)
    return CoreSnapshot(stable_id('core-snapshot',root_hash),'1.0.0',root_hash,hashes,captured_at_ms)
def compare(before:CoreSnapshot,after:CoreSnapshot,allowed_plugin_paths:tuple[str,...]=(),adr_id:str|None=None,compatibility_review_hash:str|None=None)->EngineInvarianceReport:
    changed=tuple(sorted(k for k in set(before.file_hashes)|set(after.file_hashes) if before.file_hashes.get(k)!=after.file_hashes.get(k)))
    status=InvarianceStatus.PASS if not changed else InvarianceStatus.ADR_REQUIRED
    return EngineInvarianceReport(stable_id('invariance',{'before':before.snapshot_hash,'after':after.snapshot_hash,'changed':changed}),'1.0.0',before.snapshot_hash,after.snapshot_hash,status,changed,tuple(safe_relative_path(x) for x in allowed_plugin_paths),adr_id,compatibility_review_hash)
