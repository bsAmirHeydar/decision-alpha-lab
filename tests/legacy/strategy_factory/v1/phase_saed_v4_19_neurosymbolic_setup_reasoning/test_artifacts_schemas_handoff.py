import hashlib,json,pytest
from saed_v4_neurosymbolic_setup_reasoning.validation import validate_upstream
from saed_v4_neurosymbolic_setup_reasoning.errors import IntegrityError
from saed_v4_neurosymbolic_setup_reasoning.canonical import content_hash

def test_artifacts(load,root,art):
 for f in (root/art).glob('*.JSON'):json.loads(f.read_text(encoding='utf-8'))
def test_upstream(load,root):validate_upstream(load('releases/history/strategy_factory/artifacts/saed_v4_18/V4_18_TO_V4_19_HANDOFF.JSON'))
def test_upstream_authority_mutation(load,root):
 x=load('releases/history/strategy_factory/artifacts/saed_v4_18/V4_18_TO_V4_19_HANDOFF.JSON');x['authority']['send_order']=True
 with pytest.raises(IntegrityError):validate_upstream(x)
def test_handoff(load,art):
 h=load(art+'/V4_19_TO_V4_20_HANDOFF.JSON');assert h['next_phase']=='SAED_V4_20' and all(h['entry_gates'].values()) and not h['authority']['select_live_treatment'] and not h['authority']['send_order']
def test_claims(load,art):
 c=load(art+'/GOLDEN_CLAIM_TIER_REPORT.JSON');assert c['claim_tier']=='synthetic_proof_carrying_neurosymbolic_reasoning' and not any(c[k] for k in ['real_setup_validity_established','real_mechanism_established','real_policy_value_established','production_treatment_selection','promotion_authorization','runtime_activation','production_authorization','live_trading'])
def test_baselines(load,art):assert load(art+'/GOLDEN_BASELINE_PRESERVATION.JSON')['all_preserved']
def test_exposure(load,art):
 x=load(art+'/GOLDEN_EXPOSURE_LEDGER.JSON');assert x['within_budget'] and x['counts']['hidden_evaluation_queries']==0 and x['counts']['protected_evidence_exposures']==0
@pytest.mark.parametrize('name',['GOLDEN_REASONING_TRACE.JSON','GOLDEN_PROOF_ENVELOPE.JSON','GOLDEN_BOUNDED_SYNTHESIS_REPORT.JSON','GOLDEN_COUNTEREXAMPLE_REPORT.JSON','GOLDEN_SYMBOLIC_REGRESSION_REPORT.JSON','GOLDEN_NEURAL_SYMBOLIC_DISAGREEMENT.JSON','GOLDEN_INTEGRITY_RECEIPT.JSON','GOLDEN_PROVENANCE_GRAPH.JSON','V4_19_TO_V4_20_HANDOFF.JSON'])
def test_key_artifact_exists(root,art,name):assert (root/art/name).is_file()
