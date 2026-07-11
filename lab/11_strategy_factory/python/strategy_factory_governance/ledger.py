from __future__ import annotations
from dataclasses import replace
from .models import GovernanceDecision
from .hashing import sha256_lines

class AppendOnlyDecisionLedger:
    def __init__(self, decisions=()):
        self._decisions=[]
        for decision in decisions:
            self.append_existing(decision)

    @property
    def decisions(self):
        return tuple(self._decisions)

    @property
    def last_hash(self) -> str:
        return self._decisions[-1].decision_hash if self._decisions else ""

    @property
    def chain_hash(self) -> str:
        return sha256_lines(d.decision_hash for d in self._decisions)

    def append(self, decision: GovernanceDecision) -> GovernanceDecision:
        expected_sequence=len(self._decisions)+1
        if decision.sequence != expected_sequence:
            raise ValueError("governance ledger sequence discontinuity")
        if decision.previous_decision_hash != self.last_hash:
            raise ValueError("governance ledger previous-hash mismatch")
        hashed=decision.with_hashes()
        hashed.validate()
        self._decisions.append(hashed)
        return hashed

    def append_existing(self, decision: GovernanceDecision) -> None:
        decision.validate()
        if not decision.decision_id or not decision.decision_hash:
            raise ValueError("persisted governance decision must be fully hashed")
        self.append(decision)

    def verify(self) -> None:
        previous=""
        for index, decision in enumerate(self._decisions, 1):
            if decision.sequence != index or decision.previous_decision_hash != previous:
                raise ValueError("governance ledger chain broken")
            decision.validate()
            previous=decision.decision_hash
