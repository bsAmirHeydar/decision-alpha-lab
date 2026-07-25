import pytest
@pytest.mark.parametrize("idx",range(72))
def test_intent_never_submittable(output,idx):assert output["intent_ledger"]["events"][idx]["submission_allowed"] is False
@pytest.mark.parametrize("idx",range(72))
def test_paper_never_submits(output,idx):assert output["paper_ledger"]["events"][idx]["order_submitted"] is False and output["paper_ledger"]["events"][idx]["broker_side_effect"] is False
@pytest.mark.parametrize("idx",range(72))
def test_shadow_never_submits(output,idx):assert output["shadow_ledger"]["events"][idx]["order_submitted"] is False and output["shadow_ledger"]["events"][idx]["counterfactual_only"] is True
@pytest.mark.parametrize("idx",range(72))
def test_reconciliation_has_no_live_ids(output,idx):assert output["reconciliation_ledger"]["events"][idx]["live_order_id"] is None and output["reconciliation_ledger"]["events"][idx]["live_fill_id"] is None
@pytest.mark.parametrize("idx",range(72))
def test_hash_chain_ordinals(output,idx):assert output["paper_ledger"]["events"][idx]["ordinal"]==idx and output["shadow_ledger"]["events"][idx]["ordinal"]==idx
