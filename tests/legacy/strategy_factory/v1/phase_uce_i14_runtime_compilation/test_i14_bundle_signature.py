import dataclasses,hashlib,pytest
from strategy_factory_runtime_v3.golden import *
from strategy_factory_runtime_v3.bundle import validate_bundle,compile_bundle,REQUIRED_ROLES
from strategy_factory_runtime_v3.signing import *
from strategy_factory_runtime_v3.errors import BundleValidationError

def test_golden_bundle_is_complete_and_valid():
    m,p,model,e,data=golden_bundle();validate_bundle(m,p,model,e);assert set(c.role for c in m.components)==set(REQUIRED_ROLES)
def test_partial_bundle_rejected():
    m,p,model,e,data=golden_bundle();partial=dataclasses.replace(m,components=m.components[:-1])
    with pytest.raises(BundleValidationError):validate_bundle(partial,p,model,e)
def test_preprocessing_hash_mismatch_rejected():
    m,p,model,e,data=golden_bundle();bad=dataclasses.replace(m,preprocessing_hash='0'*64)
    with pytest.raises(BundleValidationError):validate_bundle(bad,p,model,e)
def test_feature_order_mismatch_rejected():
    m,p,model,e,data=golden_bundle();bad=dataclasses.replace(m,feature_order=tuple(reversed(m.feature_order)))
    with pytest.raises(BundleValidationError):validate_bundle(bad,p,model,e)
def test_available_artifact_hashes_are_checked():
    m,p,model,e,data=golden_bundle();available={c.role:c.sha256 for c in m.components};validate_bundle(m,p,model,e,available);available['model']='0'*64
    with pytest.raises(BundleValidationError):validate_bundle(m,p,model,e,available)
def test_signature_verification_and_wrong_key():
    m,*_=golden_bundle();assert verify_manifest(m,b'uce-i14-test-secret');assert not verify_manifest(m,b'wrong')
def test_tamper_invalidates_signature():
    m,*_=golden_bundle();tampered=dataclasses.replace(m,generation=m.generation+1);assert not verify_manifest(tampered,b'uce-i14-test-secret')
def test_empty_signing_secret_rejected():
    m,*_=golden_bundle()
    with pytest.raises(BundleValidationError):sign_manifest(dataclasses.replace(m,signature=''),b'')
def test_behavior_change_changes_bundle_hash():
    m,*_=golden_bundle();assert m.bundle_hash!=dataclasses.replace(m,limitations=m.limitations+('new',)).bundle_hash
def test_component_order_is_canonicalized_by_compiler():
    m,p,model,e,data=golden_bundle();assert tuple(c.role for c in m.components)==tuple(sorted(REQUIRED_ROLES))

def test_i13_bridge_requires_exact_dependency_hashes():
    from strategy_factory_policy_v3.golden import golden_admission,golden_manual,golden_fallback,golden_authority,golden_hybrid_graph
    from strategy_factory_policy_v3.graph import compile_graph
    from strategy_factory_runtime_v3.policy_bridge import I13PolicyRuntimeBridge
    import dataclasses
    admission=golden_admission();manual=golden_manual();fallback=golden_fallback();authority=golden_authority();graph=compile_graph(golden_hybrid_graph(admission,manual,fallback,authority),admission)
    m,p,model,e,data=golden_bundle();bound=dataclasses.replace(m,policy_graph_hash=graph.spec.graph_hash,manual_policy_hash=manual.policy_hash,fallback_policy_hash=fallback.policy_hash,authority_matrix_hash=authority.matrix_hash)
    bridge=I13PolicyRuntimeBridge(bound,graph,manual,fallback,authority,admission);bridge.validate()
    with pytest.raises(BundleValidationError):I13PolicyRuntimeBridge(dataclasses.replace(bound,policy_graph_hash='0'*64),graph,manual,fallback,authority,admission).validate()

def test_i13_bridge_executes_accepted_policy_without_reinterpretation():
    from strategy_factory_policy_v3.golden import golden_admission,golden_manual,golden_fallback,golden_authority,golden_hybrid_graph,golden_occurrence,golden_output
    from strategy_factory_policy_v3.graph import compile_graph
    from strategy_factory_runtime_v3.policy_bridge import I13PolicyRuntimeBridge
    import dataclasses
    admission=golden_admission();manual=golden_manual();fallback=golden_fallback();authority=golden_authority();graph=compile_graph(golden_hybrid_graph(admission,manual,fallback,authority),admission)
    m,p,model,e,data=golden_bundle();bound=dataclasses.replace(m,policy_graph_hash=graph.spec.graph_hash,manual_policy_hash=manual.policy_hash,fallback_policy_hash=fallback.policy_hash,authority_matrix_hash=authority.matrix_hash)
    decision=I13PolicyRuntimeBridge(bound,graph,manual,fallback,authority,admission).execute(golden_occurrence(),golden_output())
    assert decision.graph_hash==graph.spec.graph_hash;assert decision.action.value in bound.output_names or decision.action.value in ('enter_long','no_action','reject','abstain')
