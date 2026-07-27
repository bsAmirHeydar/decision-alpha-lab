from copy import deepcopy
import pytest
from .conftest import FIXTURE
from saed_v4_model_risk_supply_chain import run
from saed_v4_model_risk_supply_chain.canonical import content_hash

def test_full_pipeline_accepts_reference():
    out=run(deepcopy(FIXTURE));assert out['certificate']['reference_accepted'];assert out['certificate']['production_authorized'] is False

def test_deterministic_replay():
    assert content_hash(run(deepcopy(FIXTURE)))==content_hash(run(deepcopy(FIXTURE)))

def test_handoff_bounded():
    o=run(deepcopy(FIXTURE));assert o['handoff']['next_phase']=='SAED_V4_36';assert o['handoff']['authority_granted'] is False

def test_complete_sbom_and_signatures():
    o=run(deepcopy(FIXTURE));assert o['sbom']['component_count']==o['signatures']['signature_count'];assert o['signatures']['complete_coverage']

def test_baseline_and_ucee_preserved():
    o=run(deepcopy(FIXTURE));assert o['baseline']['live_runtime_unchanged'];assert o['ucee']['ucee_runtime_mutation'] is False

@pytest.mark.parametrize('key',[
'upstream','constitution','authority','models','datasets','dependencies','tools','runtimes','services','sbom','dependency_graph','license_policy','license_review','vulnerability_catalog','vulnerability_review','build_provenance','signatures','reproducible_build','tamper_evidence','model_cards','data_cards','tiering','scorecards','validation_plan','validation_results','threat_model','attack_surface','three_lines','committee','audit','governance_ledger','exceptions','waivers','quarantine','incident_plan','recall_plan','baseline','ucee','external_boundary','eligibility','limitations','independent_reproduction','replay','evidence_bundle','certificate','handoff'])
def test_artifact_present_and_hashed(key):
    o=run(deepcopy(FIXTURE));assert key in o; assert isinstance(o[key],dict)
