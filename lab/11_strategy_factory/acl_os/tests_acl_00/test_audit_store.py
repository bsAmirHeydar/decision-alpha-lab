from __future__ import annotations
import json
from pathlib import Path
import pytest

from tools.strategy_factory.acl_os.acl_00.audit import AuditLedger
from tools.strategy_factory.acl_os.acl_00.errors import IntegrityError, ConcurrencyError
from tools.strategy_factory.acl_os.acl_00.store import InMemoryStateStore, SubjectState
from tools.strategy_factory.acl_os.acl_00.types import LifecycleState


def test_audit_chain_roundtrip(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    ledger = AuditLedger(path)
    ledger.append("A", "TEN_A", "CTX_A", "USR_A", {"x": 1})
    ledger.append("B", "TEN_A", "CTX_A", "USR_B", {"x": 2})
    assert ledger.verify()
    assert AuditLedger(path).head == ledger.head


def test_audit_tamper_detected(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    ledger = AuditLedger(path)
    ledger.append("A", "TEN_A", "CTX_A", "USR_A", {"x": 1})
    rows = path.read_text(encoding="utf-8").splitlines()
    obj = json.loads(rows[0])
    obj["actor_id"] = "ATTACKER"
    path.write_text(json.dumps(obj) + "\n", encoding="utf-8")
    with pytest.raises(IntegrityError):
        AuditLedger(path)


def test_store_compare_and_set():
    store = InMemoryStateStore()
    store.seed(SubjectState("CTX_A", "TEN_A", LifecycleState.DRAFT_CONTEXT, 0))
    result = store.compare_and_set(
        "CTX_A",
        "TEN_A",
        0,
        LifecycleState.DRAFT_CONTEXT,
        LifecycleState.SEMANTICALLY_VALIDATED,
    )
    assert result.revision == 1


def test_store_rejects_stale_revision():
    store = InMemoryStateStore()
    store.seed(SubjectState("CTX_A", "TEN_A", LifecycleState.DRAFT_CONTEXT, 1))
    with pytest.raises(ConcurrencyError):
        store.compare_and_set(
            "CTX_A",
            "TEN_A",
            0,
            LifecycleState.DRAFT_CONTEXT,
            LifecycleState.SEMANTICALLY_VALIDATED,
        )


def test_store_rejects_wrong_from_state():
    store = InMemoryStateStore()
    store.seed(SubjectState("CTX_A", "TEN_A", LifecycleState.CONTEXT_COMPILED, 1))
    with pytest.raises(ConcurrencyError):
        store.compare_and_set(
            "CTX_A",
            "TEN_A",
            1,
            LifecycleState.DRAFT_CONTEXT,
            LifecycleState.SEMANTICALLY_VALIDATED,
        )
