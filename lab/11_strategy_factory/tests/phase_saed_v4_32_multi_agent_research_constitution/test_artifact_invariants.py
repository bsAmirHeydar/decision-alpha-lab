import pytest
@pytest.mark.parametrize("key",["upstream","constitution","constitution_coverage","roles","agents","capabilities","separation","tasks","delegation","tokens","plan","scheduler_trace","memory","budgets","budget_ledger","sources","exposure","prompt_ledger","claim_graph","attribution","contradictions","adversarial_report","blocking_issues","checkpoints","quorum","incidents","policy_ledger","contract_closure","known_time","security","model_risk","limitations","reproduction","replay","authority","evidence_bundle","certificate","handoff"])
def test_artifact_is_research_only(result,key): assert result[key]["research_only"] is True
@pytest.mark.parametrize("key",["upstream","constitution","roles","agents","capabilities","tasks","sources","claim_graph","certificate","handoff"])
def test_artifact_has_identity_and_hash(result,key):
 d=result[key]; ids=[k for k in d if k.endswith('_id')]; hashes=[k for k in d if k.endswith('_hash')]; assert ids and hashes
