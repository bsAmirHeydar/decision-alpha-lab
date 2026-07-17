import pytest
@pytest.mark.parametrize("index",range(15))
def test_each_obligation_discharged(result,index): assert result["proof_ledger"]["statuses"][index]["passed"]
@pytest.mark.parametrize("index",range(15))
def test_each_obligation_has_evidence(result,index): assert result["proof_ledger"]["statuses"][index]["evidence_hashes"]
def test_proof_coverage_complete(result): assert result["proof_coverage"]["complete"]
