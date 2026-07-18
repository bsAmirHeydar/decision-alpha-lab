import copy
import json
import pytest

from tools.strategy_factory.lcm.lcm_00.errors import IntegrityError
from tools.strategy_factory.lcm.lcm_00.event_ledger import build_event_ledger, verify_event_ledger


def test_reference_event_chain_verifies(baseline_root):
    ledger=json.loads((baseline_root/"events/freeze_event_ledger.json").read_text(encoding="utf-8"))
    verify_event_ledger(ledger)
    assert ledger["event_count"] == 8


def test_event_tamper_is_detected(baseline_root):
    ledger=json.loads((baseline_root/"events/freeze_event_ledger.json").read_text(encoding="utf-8"))
    ledger["events"][1]["payload"]["x"]="tamper"
    with pytest.raises(IntegrityError):
        verify_event_ledger(ledger)


def test_provenance_denies_mutation_and_authority(baseline_root):
    graph=json.loads((baseline_root/"lineage/baseline_provenance_graph.json").read_text(encoding="utf-8"))
    assert graph["source_behavior_mutated"] is False
    assert graph["source_file_moved"] is False
    assert graph["source_file_deleted"] is False
    assert graph["execution_authority_created"] is False
    assert graph["capital_authority_created"] is False
