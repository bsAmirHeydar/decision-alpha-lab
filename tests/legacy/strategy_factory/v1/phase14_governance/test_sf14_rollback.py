from dataclasses import replace
from strategy_factory_governance.examples import *
from strategy_factory_governance import *

def test_rollback_promotes_declared_target_and_retires_source():
    scope,evidence,policy,evaluation,r,old,snapshot,release,report=reference_governance_bundle()
    # Keep the old champion as rollback target by first suspending it, then create/promote a new champion.
    old=r.suspend(old.entry_id,"DRIFT_ALERT",at=1_700_000_010_000)
    e2=replace(evidence,bundle_id="bundle2",model_version="2.0.0",model_artifact_hash=evidence.model_artifact_hash[:-1]+"2",bundle_hash="").with_hash()
    ev2=evaluate_promotion(e2,scope,policy,reference_measurements(),evaluated_at_utc_msc=1_700_000_011_000,evaluator_id="test")
    n=r.register(model_id=e2.model_id,model_version=e2.model_version,model_artifact_hash=e2.model_artifact_hash,scope_id=scope.scope_id,evidence_bundle_hash=e2.bundle_hash,created_at_utc_msc=1_700_000_012_000)
    n=r.validate_evidence(n.entry_id,ev2,at=1_700_000_013_000);n=r.nominate(n.entry_id,at=1_700_000_014_000);n=r.assign_challenger(n.entry_id,policy,at=1_700_000_015_000);n=r.promote_champion(n.entry_id,at=1_700_000_016_000)
    snap=build_registry_snapshot(r,generated_at_utc_msc=1_700_000_017_000)
    plan=RollbackPlan("rollback_1",scope.scope_id,n.entry_id,old.entry_id,("DRIFT","SAFETY"),snap.snapshot_hash,"risk_committee",1_700_000_018_000).with_hash()
    restored=r.rollback(plan,at=1_700_000_019_000)
    assert restored.entry_id==old.entry_id and restored.state==RegistryState.CHAMPION
    assert r.get(n.entry_id).state==RegistryState.RETIRED
