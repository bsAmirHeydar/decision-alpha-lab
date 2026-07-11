from __future__ import annotations
from .models import *
from .enums import *
from .promotion import evaluate_promotion
from .registry import ModelRegistry
from .snapshots import build_registry_snapshot
from .release import build_release_manifest
from .hashing import sha256_text, stable_id

def _h(name):return sha256_text("sf14/reference/"+name)

def reference_inventory():
    digests=(
      ArtifactDigest("model","artifacts/model.bin",ArtifactRole.MODEL,"application/octet-stream",128,_h("model_file"),"",True).with_id(),
      ArtifactDigest("transform","artifacts/transform.json",ArtifactRole.TRANSFORM,"application/json",256,_h("transform_file"),"alpha_lab.strategy_factory/transform_state@1.0.0",True).with_id(),
      ArtifactDigest("model_card","artifacts/model_card.json",ArtifactRole.MODEL_CARD,"application/json",512,_h("model_card_file"),"alpha_lab.strategy_factory/model_card@1.0.0",True).with_id(),
    )
    return ArtifactInventory("sf14_reference_inventory","1.0.0",digests,1_700_000_000_000).with_hash()

def reference_scope():
    return RegistryScope("reference_strategy","sf06.reference_sweep","1.0.0","major_indices",
        "m5_h1","research_default",_h("feature_schema"),_h("label_contract")).with_id()

def reference_evidence():
    return ModelEvidenceBundle("sf14_reference_bundle","reference_logistic","1.0.0",
        _h("model_artifact"),_h("transform"),_h("calibration"),_h("feature_schema"),
        _h("label_contract"),_h("dataset"),_h("training_plan"),_h("training_report"),
        _h("model_card"),_h("test_oos_predictions"),_h("anti_overfit_report"),
        _h("phase12_promotion_decision"),"revision_sf14",reference_inventory().inventory_hash,"",
        1_700_000_000_000).with_hash()

def reference_policy(require_signature=False):
    return PromotionPolicy("default_research_promotion","1.0.0",100,0.52,0.50,0.10,0.08,0.75,
        require_verified_attestation=require_signature,max_challengers_per_scope=4).with_hash()

def reference_measurements(attestation_verified=False):
    return PromotionMeasurements(True,True,240,0.61,0.57,0.035,0.875,True,True,True,attestation_verified)

def reference_governance_bundle():
    scope=reference_scope();evidence=reference_evidence();policy=reference_policy()
    evaluation=evaluate_promotion(evidence,scope,policy,reference_measurements(),
        evaluated_at_utc_msc=1_700_000_001_000,evaluator_id="sf14_reference_evaluator")
    registry=ModelRegistry()
    entry=registry.register(model_id=evidence.model_id,model_version=evidence.model_version,
        model_artifact_hash=evidence.model_artifact_hash,scope_id=scope.scope_id,
        evidence_bundle_hash=evidence.bundle_hash,created_at_utc_msc=1_700_000_002_000)
    entry=registry.validate_evidence(entry.entry_id,evaluation,at=1_700_000_003_000)
    entry=registry.nominate(entry.entry_id,at=1_700_000_004_000)
    entry=registry.assign_challenger(entry.entry_id,policy,at=1_700_000_005_000)
    entry=registry.promote_champion(entry.entry_id,at=1_700_000_006_000)
    snapshot=build_registry_snapshot(registry,generated_at_utc_msc=1_700_000_007_000)
    release=build_release_manifest(entry,evidence,snapshot,release_version="1.0.0",
        channel=ReleaseChannel.INFERENCE_CANDIDATE,created_at_utc_msc=1_700_000_008_000)
    report=GovernanceReportManifest("sf14_reference_report",evidence.bundle_hash,
        evaluation.evaluation_hash,snapshot.snapshot_hash,release.release_hash,"",
        registry.ledger.chain_hash,1_700_000_009_000).with_hash()
    return scope,evidence,policy,evaluation,registry,entry,snapshot,release,report
