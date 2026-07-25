import json,pytest
NAMES=['GOLDEN_UPSTREAM_VALIDATION.JSON','GOLDEN_INTAKE_DECISIONS.JSON','GOLDEN_SUPPLY_CHAIN_ATTESTATIONS.JSON','GOLDEN_CONTAMINATION_AUDIT.JSON','GOLDEN_TOKEN_SEQUENCE.JSON','GOLDEN_COMPUTE_EXPOSURE_LEDGER.JSON','GOLDEN_ADAPTER_FEATURES.JSON','GOLDEN_CALIBRATION_REPORT.JSON','GOLDEN_DOMAIN_SHIFT_REPORT.JSON','GOLDEN_CANDIDATE_METRICS.JSON','GOLDEN_FUTURE_SUFFIX_AUDITS.JSON','GOLDEN_FAIL_CLOSED_AUDITS.JSON','GOLDEN_CANDIDATE_CHECKPOINTS.JSON','GOLDEN_TOURNAMENT.JSON','GOLDEN_CHECKPOINT_REGISTRY.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','GOLDEN_REPLAY_RECEIPT.JSON','PROVENANCE.JSON','V4_14_TO_V4_15_HANDOFF.JSON','CLAIM_LEDGER.JSON','SBOM.JSON','INCIDENT_TEMPLATE.JSON','AUTHORITY_BOUNDARY.JSON','CONFORMANCE_RESULTS.JSON','CONTRACT_VALIDATION_MAP.JSON']
@pytest.mark.parametrize('name',NAMES)
def test_artifact_exists_and_json(root,name):
 p=root/'releases/history/strategy_factory/artifacts/saed_v4_14'/name;assert p.is_file();json.loads(p.read_text())
def test_claims_conservative(load):
 c=load('releases/history/strategy_factory/artifacts/saed_v4_14/CLAIM_LEDGER.JSON')['claims'];assert c['foundation_model_adapter_boundary_implemented'] and not c['real_external_model_loaded'] and not c['production_authorization']
def test_conformance_passed(load):assert load('releases/history/strategy_factory/artifacts/saed_v4_14/CONFORMANCE_RESULTS.JSON')['passed']
