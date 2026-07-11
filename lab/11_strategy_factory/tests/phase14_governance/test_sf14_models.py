from strategy_factory_governance.examples import reference_scope,reference_evidence,reference_policy

def test_reference_contract_hashes_are_stable_and_valid():
    scope=reference_scope();scope.validate();assert scope.scope_id==scope.with_id().scope_id
    evidence=reference_evidence();evidence.validate();assert evidence.bundle_hash==evidence.with_hash().bundle_hash
    policy=reference_policy();policy.validate();assert policy.policy_hash==policy.with_hash().policy_hash

def test_scope_rejects_tampered_identity():
    from dataclasses import replace
    import pytest
    scope=replace(reference_scope(),scope_id="scope_bad")
    with pytest.raises(ValueError,match="scope identity"):scope.validate()
