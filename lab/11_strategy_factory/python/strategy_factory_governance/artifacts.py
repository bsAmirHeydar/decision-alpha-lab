from __future__ import annotations
from pathlib import Path
from dataclasses import replace
from .models import ArtifactDigest, ArtifactInventory, AuthenticityAttestation
from .hashing import sha256_bytes, sha256_lines

def digest_file(path: Path, *, root: Path, logical_name: str, role, media_type: str,
                schema_id: str = "", required: bool = True) -> ArtifactDigest:
    resolved = path.resolve()
    base = root.resolve()
    try:
        rel = resolved.relative_to(base).as_posix()
    except ValueError as exc:
        raise ValueError("artifact path escapes declared root") from exc
    data = resolved.read_bytes()
    digest = ArtifactDigest(logical_name, rel, role, media_type, len(data), sha256_bytes(data),
                            schema_id, required).with_id()
    digest.validate()
    return digest

def build_inventory(inventory_id: str, inventory_version: str, digests, generated_at_utc_msc: int) -> ArtifactInventory:
    inventory=ArtifactInventory(inventory_id,inventory_version,tuple(digests),generated_at_utc_msc).with_hash()
    inventory.validate();return inventory

def inventory_hash(digests) -> str:
    ordered = sorted(digests, key=lambda d: (d.logical_name, d.relative_path))
    validate_inventory(ordered)
    return sha256_lines(d.digest_id or d.with_id().digest_id for d in ordered)

def validate_inventory(digests, required_names=()) -> None:
    names=set(); paths=set()
    for digest in digests:
        digest.validate()
        if digest.logical_name in names:
            raise ValueError("duplicate artifact logical name")
        if digest.relative_path in paths:
            raise ValueError("duplicate artifact relative path")
        names.add(digest.logical_name); paths.add(digest.relative_path)
    missing = sorted(set(required_names)-names)
    if missing:
        raise ValueError("missing required artifacts: " + ", ".join(missing))

def validate_attestation(attestation: AuthenticityAttestation, expected_inventory_hash: str,
                         require_verified: bool) -> None:
    attestation.validate()
    if attestation.subject_inventory_hash != expected_inventory_hash:
        raise ValueError("attestation subject does not match artifact inventory")
    if require_verified and not attestation.verified:
        raise ValueError("verified authenticity attestation is required")
