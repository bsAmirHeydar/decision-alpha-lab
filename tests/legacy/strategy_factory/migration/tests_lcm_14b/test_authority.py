def test_no_authority(load):
 h=load("LCM14B_TO_LCM15A_HANDOFF.json")
 for k in ("runtime_authority_created","live_order_authority_created","capital_authority_created","deletion_authority_created"): assert h[k] is False
 assert load("quarantine_observation_receipt.json")["deletion_performed"] is False
