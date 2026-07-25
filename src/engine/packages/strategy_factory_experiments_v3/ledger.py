"""Append-only, hash-chained selection ledger for UCE-I11."""

from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, Mapping

from .canonical import canonical_sha256, stable_id
from .contracts import SelectionLedgerEntry
from .enums import LedgerAction
from .errors import ExperimentError


class SelectionLedger:
    def __init__(self, experiment_id: str, manifest_hash: str) -> None:
        self.experiment_id = experiment_id
        self.manifest_hash = manifest_hash
        self._entries: list[SelectionLedgerEntry] = []

    @property
    def entries(self) -> tuple[SelectionLedgerEntry, ...]:
        return tuple(self._entries)

    @property
    def head_hash(self) -> str:
        return self._entries[-1].entry_hash if self._entries else ""

    def append(
        self,
        *,
        trial_id: str,
        node_id: str,
        action: LedgerAction,
        reason_code: str,
        metrics: Mapping[str, float] | None = None,
        artifact_hashes: Iterable[str] = (),
        actor: str = "uce_i11_scheduler",
    ) -> SelectionLedgerEntry:
        sequence = len(self._entries)
        previous = self.head_hash
        body = {
            "sequence": sequence,
            "experiment_id": self.experiment_id,
            "manifest_hash": self.manifest_hash,
            "trial_id": trial_id,
            "node_id": node_id,
            "action": action.value,
            "reason_code": reason_code,
            "metrics": dict(metrics or {}),
            "artifact_hashes": tuple(artifact_hashes),
            "actor": actor,
            "previous_entry_hash": previous,
        }
        entry_hash = canonical_sha256(body)
        entry = SelectionLedgerEntry(
            entry_id=stable_id("uceledger", body),
            sequence=sequence,
            experiment_id=self.experiment_id,
            manifest_hash=self.manifest_hash,
            trial_id=trial_id,
            node_id=node_id,
            action=action,
            reason_code=reason_code,
            metrics=dict(metrics or {}),
            artifact_hashes=tuple(artifact_hashes),
            actor=actor,
            previous_entry_hash=previous,
            entry_hash=entry_hash,
        )
        self._entries.append(entry)
        return entry

    def verify(self) -> bool:
        previous = ""
        for expected_sequence, entry in enumerate(self._entries):
            if entry.sequence != expected_sequence or entry.previous_entry_hash != previous:
                return False
            body = {
                "sequence": entry.sequence,
                "experiment_id": entry.experiment_id,
                "manifest_hash": entry.manifest_hash,
                "trial_id": entry.trial_id,
                "node_id": entry.node_id,
                "action": entry.action.value,
                "reason_code": entry.reason_code,
                "metrics": dict(entry.metrics),
                "artifact_hashes": tuple(entry.artifact_hashes),
                "actor": entry.actor,
                "previous_entry_hash": entry.previous_entry_hash,
            }
            if canonical_sha256(body) != entry.entry_hash:
                return False
            previous = entry.entry_hash
        return True

    def assert_report_models_accounted(self, trial_ids: Iterable[str]) -> None:
        selected = {
            entry.trial_id
            for entry in self._entries
            if entry.action in (LedgerAction.SELECTED, LedgerAction.ENSEMBLED)
        }
        missing = sorted(set(trial_ids) - selected)
        if missing:
            raise ExperimentError(
                "report_model_missing_from_ledger",
                "every model in a report must exist as selected/ensembled in the ledger",
                {"missing_trial_ids": missing},
            )

    def canonical_snapshot(self) -> tuple[dict, ...]:
        return tuple(asdict(entry) for entry in self._entries)
