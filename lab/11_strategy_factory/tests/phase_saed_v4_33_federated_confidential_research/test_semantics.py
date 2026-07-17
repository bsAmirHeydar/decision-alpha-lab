import pytest
@pytest.mark.parametrize("key",["upstream","constitution","cells","attestations","classifications","residency","protocols","study","eligibility","manifests","receipts","clipping","envelopes","signatures","privacy_policy","privacy_budget","aggregation_plan","aggregation_transcript","dropout","screening","global_model","provenance","exposure","protected_policy","human_reviews","adversarial_review","incidents","contract_closure","known_time","security","model_risk","limitations","reproduction","replay","authority","evidence_bundle","certificate","handoff"])
def test_all_outputs_present(result,key): assert key in result and isinstance(result[key],dict)
@pytest.mark.parametrize("cid",["CELL-AMS-001","CELL-FRA-001","CELL-LON-001","CELL-ZRH-001"])
def test_each_cell_accounted(result,cid):
 assert cid in [x["cell_id"] for x in result["cells"]["cells"]]
 assert cid in [x["cell_id"] for x in result["receipts"]["receipts"]]
 assert cid in [x["cell_id"] for x in result["envelopes"]["envelopes"]]
@pytest.mark.parametrize("gate",["upstream_verified","constitution_frozen","cells_attested","raw_data_local","eligibility_threshold","privacy_budget_respected","aggregation_threshold","raw_vectors_not_disclosed","provenance_complete","exposure_complete","human_review","adversarial_review","incidents_contained","deterministic_replay","zero_authority"])
def test_certificate_gate(result,gate): assert result["certificate"]["gates"][gate]
@pytest.mark.parametrize("forbidden",["promotion","runtime","risk_allocation","execution","production","online_learning","live_trading","credential_distribution","raw_data_export"])
def test_no_authority(result,forbidden): assert result["authority"]["authority"][forbidden] is False
