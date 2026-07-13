from __future__ import annotations
from .canonical import canonical_sha256,stable_id
from .contracts import WindowStoreSnapshot
from .enums import StoreHealth,PairWindowHealth

def build_store_snapshot(config,source_dataset_snapshot_id,source_revision_id,pair_windows,references,created_utc_ms):
    windows=tuple(sorted(pair_windows,key=lambda w:(w.descriptor.start_utc_ms,w.descriptor.kind.value,w.pair_window_id)))
    refs=tuple(sorted(references,key=lambda r:(r.source_trading_date,r.source_window_kind.value,r.canonical_symbol,r.side.value,r.reference_id)))
    if any(w.health is PairWindowHealth.BLOCKED for w in windows): health=StoreHealth.BLOCKED;reasons=('FP_RRC_STORE_BLOCKED',)
    elif any(w.health is PairWindowHealth.DEGRADED for w in windows): health=StoreHealth.DEGRADED;reasons=('FP_RRC_STORE_DEGRADED',)
    else: health=StoreHealth.READY;reasons=('FP_RRC_STORE_READY',)
    index_material={'window_keys':[(w.descriptor.trading_date,w.descriptor.kind,w.pair_window_id) for w in windows],'reference_keys':[(r.canonical_symbol,r.side,r.source_pair_window_id,r.reference_id) for r in refs]}
    index_hash=canonical_sha256(index_material)
    material={'pair_id':config.pair_id,'config_hash':config.config_hash,'dataset':source_dataset_snapshot_id,'revision':source_revision_id,'windows':[w.semantic_hash for w in windows],'references':[r.semantic_hash for r in refs],'health':health,'index_hash':index_hash}
    sem=canonical_sha256(material)
    return WindowStoreSnapshot(stable_id('FPSTORE',material,32),config.pair_id,config.config_hash,source_dataset_snapshot_id,source_revision_id,windows,refs,health,reasons,created_utc_ms,index_hash,sem)

def window_index(snapshot): return {(w.descriptor.trading_date,w.descriptor.kind):w for w in snapshot.pair_windows}
def reference_index(snapshot): return {(r.canonical_symbol,r.side,r.source_pair_window_id):r for r in snapshot.references}
def get_window(snapshot,trading_date,kind): return window_index(snapshot).get((trading_date,kind))
def get_references_for_window(snapshot,pair_window_id): return tuple(r for r in snapshot.references if r.source_pair_window_id==pair_window_id)


def evolve_snapshot(snapshot,updated_reference,created_utc_ms):
    refs=[];found=False
    for ref in snapshot.references:
        if ref.reference_id==updated_reference.reference_id:
            refs.append(updated_reference);found=True
        else:refs.append(ref)
    if not found: raise ValueError('reference not found in snapshot')
    refs=tuple(sorted(refs,key=lambda r:(r.source_trading_date,r.source_window_kind.value,r.canonical_symbol,r.side.value,r.reference_id)))
    index_material={'window_keys':[(w.descriptor.trading_date,w.descriptor.kind,w.pair_window_id) for w in snapshot.pair_windows],'reference_keys':[(r.canonical_symbol,r.side,r.source_pair_window_id,r.reference_id,r.state,r.state_sequence) for r in refs]}
    index_hash=canonical_sha256(index_material)
    material={'pair_id':snapshot.pair_id,'config_hash':snapshot.config_hash,'dataset':snapshot.source_dataset_snapshot_id,'revision':snapshot.source_revision_id,'windows':[w.semantic_hash for w in snapshot.pair_windows],'references':[(r.semantic_hash,r.state,r.state_sequence,r.last_transition_utc_ms) for r in refs],'health':snapshot.health,'index_hash':index_hash}
    sem=canonical_sha256(material)
    return WindowStoreSnapshot(stable_id('FPSTORE',material,32),snapshot.pair_id,snapshot.config_hash,snapshot.source_dataset_snapshot_id,snapshot.source_revision_id,snapshot.pair_windows,refs,snapshot.health,snapshot.reason_codes,created_utc_ms,index_hash,sem)
