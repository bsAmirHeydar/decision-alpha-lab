from _common import AR,load
cert=load(AR/"GOLDEN_FEDERATED_CONFIDENTIAL_RESEARCH_CERTIFICATE.JSON"); auth=load(AR/"GOLDEN_AUTHORITY_BOUNDARY.JSON"); res=load(AR/"GOLDEN_RESIDENCY_POLICY.JSON"); priv=load(AR/"GOLDEN_PRIVACY_BUDGET_LEDGER.JSON")
assert cert["accepted_reference"] and cert["all_gates_passed"]
assert auth["all_zero"] and all(v is False for v in auth["authority"].values())
assert res["all_raw_data_local"] and priv["budget_respected"]
assert not cert["real_federated_runtime_claim"] and not cert["real_confidentiality_claim"]
print("V4-33 governance passed")
