from __future__ import annotations
from .models import ModelReleaseManifest
from .enums import RegistryState, ReleaseChannel
from .hashing import stable_id

def build_release_manifest(entry, evidence, snapshot, *, release_version: str,
                           channel: ReleaseChannel, created_at_utc_msc: int) -> ModelReleaseManifest:
    entry.validate(); evidence.validate(); snapshot.validate()
    if entry.state not in (RegistryState.CHALLENGER,RegistryState.CHAMPION):
        raise ValueError("only challenger or champion entries may receive a release manifest")
    if entry.evidence_bundle_hash != evidence.bundle_hash:
        raise ValueError("release entry and evidence bundle mismatch")
    if entry.entry_hash not in snapshot.entry_hashes:
        raise ValueError("release entry is absent from registry snapshot")
    release_id=stable_id("mrel", "|".join([entry.entry_hash,snapshot.snapshot_hash,release_version,str(int(channel))]))
    result=ModelReleaseManifest(release_id,release_version,channel,snapshot.snapshot_hash,
        entry.entry_hash,evidence.model_artifact_hash,evidence.transform_hash,evidence.calibration_hash,
        evidence.feature_schema_hash,evidence.label_contract_hash,evidence.artifact_inventory_hash,
        evidence.attestation_hash,created_at_utc_msc).with_hash()
    result.validate();return result
