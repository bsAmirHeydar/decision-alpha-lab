import pytest
@pytest.mark.parametrize("index",range(18))
def test_each_mutation_killed(result,index):
 record=result["mutation_scorecard"]["records"][index]; assert record["killed"] and set(record["expected_detectors"])&set(record["observed_detectors"])
@pytest.mark.parametrize("index",range(18))
def test_each_mutant_has_hash(result,index): assert len(result["mutation_scorecard"]["records"][index]["mutant_model_hash"])==64
def test_counterexamples_preserved(result): assert result["counterexample_ledger"]["all_failures_preserved"] and not result["counterexample_ledger"]["counterexample_discard_allowed"]
