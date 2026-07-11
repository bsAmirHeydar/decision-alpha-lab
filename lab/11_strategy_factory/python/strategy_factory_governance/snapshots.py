from __future__ import annotations
from .models import RegistrySnapshot
from .enums import RegistryState
from .hashing import stable_id

def build_registry_snapshot(registry, *, generated_at_utc_msc: int) -> RegistrySnapshot:
    registry.ledger.verify()
    entries=registry.entries
    champions=tuple(sorted(e.entry_id for e in entries if e.state==RegistryState.CHAMPION))
    challengers=tuple(sorted(e.entry_id for e in entries if e.state==RegistryState.CHALLENGER))
    scope_counts={}
    for entry in entries:
        if entry.state==RegistryState.CHAMPION:
            scope_counts[entry.scope_id]=scope_counts.get(entry.scope_id,0)+1
    if any(v>1 for v in scope_counts.values()):
        raise ValueError("snapshot cannot contain multiple champions in one scope")
    snapshot_id=stable_id("rsnap", "|".join([registry.registry_version,registry.ledger.chain_hash,
                                             str(len(registry.ledger.decisions))]))
    snapshot=RegistrySnapshot(snapshot_id,registry.registry_version,len(registry.ledger.decisions),
        registry.ledger.chain_hash,tuple(e.entry_hash for e in entries),champions,challengers,
        generated_at_utc_msc).with_hash()
    snapshot.validate();return snapshot
