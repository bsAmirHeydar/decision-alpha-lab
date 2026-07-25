from dataclasses import replace
import pytest
from strategy_factory_governance.examples import *
from strategy_factory_governance import *

def _eligible(scope,evidence,policy,at=10):
    return evaluate_promotion(evidence,scope,policy,reference_measurements(),evaluated_at_utc_msc=at,evaluator_id="test")

def _to_challenger(registry,scope,evidence,policy,version,at):
    e=replace(evidence,model_version=version,model_artifact_hash=evidence.model_artifact_hash[:-1]+str(int(version[0])%10),bundle_id=evidence.bundle_id+version,bundle_hash="").with_hash()
    ev=_eligible(scope,e,policy,at)
    x=registry.register(model_id=e.model_id,model_version=e.model_version,model_artifact_hash=e.model_artifact_hash,
        scope_id=scope.scope_id,evidence_bundle_hash=e.bundle_hash,created_at_utc_msc=at)
    x=registry.validate_evidence(x.entry_id,ev,at=at+1);x=registry.nominate(x.entry_id,at=at+2)
    return registry.assign_challenger(x.entry_id,policy,at=at+3),e,ev

def test_registry_enforces_exact_version_uniqueness():
    scope=reference_scope();e=reference_evidence();r=ModelRegistry()
    r.register(model_id=e.model_id,model_version=e.model_version,model_artifact_hash=e.model_artifact_hash,
        scope_id=scope.scope_id,evidence_bundle_hash=e.bundle_hash,created_at_utc_msc=1)
    with pytest.raises(ValueError,match="duplicate exact model version"):
        r.register(model_id=e.model_id,model_version=e.model_version,model_artifact_hash=e.model_artifact_hash,
            scope_id=scope.scope_id,evidence_bundle_hash=e.bundle_hash,created_at_utc_msc=2)

def test_new_champion_atomically_retires_previous_champion():
    scope=reference_scope();base=reference_evidence();policy=reference_policy();r=ModelRegistry()
    a,_,_= _to_challenger(r,scope,base,policy,"1.0.0",100)
    a=r.promote_champion(a.entry_id,at=110)
    b,_,_= _to_challenger(r,scope,base,policy,"2.0.0",200)
    b=r.promote_champion(b.entry_id,at=210)
    assert r.get(a.entry_id).state==RegistryState.RETIRED
    assert r.champion_for_scope(scope.scope_id).entry_id==b.entry_id
    assert r.get(b.entry_id).supersedes_entry_id==a.entry_id

def test_ineligible_evaluation_cannot_enter_governed_state():
    scope=reference_scope();e=reference_evidence();p=reference_policy();r=ModelRegistry()
    bad=evaluate_promotion(e,scope,p,replace(reference_measurements(),test_score=-1.0),evaluated_at_utc_msc=2,evaluator_id="test")
    x=r.register(model_id=e.model_id,model_version=e.model_version,model_artifact_hash=e.model_artifact_hash,
        scope_id=scope.scope_id,evidence_bundle_hash=e.bundle_hash,created_at_utc_msc=1)
    with pytest.raises(ValueError,match="ineligible model"):
        r.validate_evidence(x.entry_id,bad,at=3)
