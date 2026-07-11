from dataclasses import replace
import pytest
from strategy_factory_governance.examples import reference_governance_bundle
from strategy_factory_governance import AppendOnlyDecisionLedger

def test_reference_ledger_is_contiguous_and_hash_chained():
    *_,registry,entry,snapshot,release,report=reference_governance_bundle()
    registry.ledger.verify();assert len(registry.ledger.decisions)==5
    assert registry.ledger.chain_hash==snapshot.decision_chain_hash

def test_tampered_previous_hash_is_rejected():
    *_,registry,entry,snapshot,release,report=reference_governance_bundle()
    first=registry.ledger.decisions[0]
    second=replace(registry.ledger.decisions[1],previous_decision_hash="bad",decision_hash="")
    ledger=AppendOnlyDecisionLedger([first])
    with pytest.raises(ValueError,match="previous-hash"):ledger.append(second)
