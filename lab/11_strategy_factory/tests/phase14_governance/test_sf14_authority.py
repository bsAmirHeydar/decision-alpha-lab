from dataclasses import replace
import pytest
from strategy_factory_governance.examples import reference_evidence,reference_governance_bundle

def test_evidence_and_registry_remain_no_authority():
    evidence=replace(reference_evidence(),no_execution_authority=False,bundle_hash="")
    with pytest.raises(ValueError,match="execution authority"):evidence.validate()
    *_,entry,snapshot,release,report=reference_governance_bundle()
    assert entry.no_execution_authority and snapshot.no_execution_authority and release.no_execution_authority
