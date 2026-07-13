"""Transfer/pretraining boundary checks for UCE-I10."""

from __future__ import annotations

from collections.abc import Sequence

from .canonical import canonical_sha256, stable_id
from .contracts import TransferBoundary
from .enums import TransferDecision


def evaluate_transfer_boundary(
    source_dataset_manifest_hash: str,
    target_dataset_manifest_hash: str,
    source_row_ids: Sequence[str],
    target_train_row_ids: Sequence[str],
    target_final_test_row_ids: Sequence[str],
    representation_frozen: bool,
) -> TransferBoundary:
    blockers: list[str] = []
    source = set(source_row_ids)
    target_train = set(target_train_row_ids)
    target_test = set(target_final_test_row_ids)
    if not source_dataset_manifest_hash or not target_dataset_manifest_hash:
        blockers.append("dataset_manifest_hash_missing")
    if not source:
        blockers.append("source_pretraining_rows_missing")
    if not target_train:
        blockers.append("target_training_rows_missing")
    if target_train & target_test:
        blockers.append("target_train_final_test_overlap")
    if source & target_test:
        blockers.append("source_contains_target_final_test_rows")
    decision = TransferDecision.REJECT if blockers else TransferDecision.ACCEPT
    material = {
        "source_dataset_manifest_hash": source_dataset_manifest_hash,
        "target_dataset_manifest_hash": target_dataset_manifest_hash,
        "source_row_ids": tuple(sorted(source)),
        "target_train_row_ids": tuple(sorted(target_train)),
        "target_final_test_row_ids": tuple(sorted(target_test)),
        "representation_frozen": bool(representation_frozen),
        "decision": decision.value,
        "blockers": blockers,
    }
    return TransferBoundary(
        boundary_id=stable_id("ucetransfer", material),
        source_dataset_manifest_hash=source_dataset_manifest_hash,
        target_dataset_manifest_hash=target_dataset_manifest_hash,
        source_row_ids_hash=canonical_sha256(tuple(sorted(source))),
        target_train_row_ids_hash=canonical_sha256(tuple(sorted(target_train))),
        target_final_test_row_ids_hash=canonical_sha256(tuple(sorted(target_test))),
        representation_frozen=bool(representation_frozen),
        decision=decision,
        blockers=tuple(blockers),
        evidence_hash=canonical_sha256(material),
    )
