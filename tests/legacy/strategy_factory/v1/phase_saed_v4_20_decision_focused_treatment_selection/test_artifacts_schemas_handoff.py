from tools.repository_paths import find_repository_root
from pathlib import Path
import json,pytest
from saed_v4_decision_focused_treatment_selection.certificates import verify_selection_certificate
ROOT=find_repository_root(__file__);ART=ROOT/'releases/history/strategy_factory/artifacts/saed_v4_20';SCH=ROOT/'schemas/legacy/strategy_factory/saed_v4_20'
load=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))

def test_contract_map_closed():
 m=load(ART/'CONTRACT_VALIDATION_MAP.JSON');assert m['contract_count']==len(m['contracts']) and m['unknown_fields_forbidden'] and m['contract_count']>=40

def test_golden_certificate_valid():assert verify_selection_certificate(load(ART/'GOLDEN_SELECTION_CERTIFICATE.JSON'))
def test_handoff_is_narrow():
 h=load(ART/'V4_20_TO_V4_21_HANDOFF.JSON');assert h['next_phase']=='SAED_V4_21' and h['research_only'] and all(h['entry_gates'].values()) and not any(h['authority'].values())
def test_claim_ceiling():
 c=load(ART/'GOLDEN_CLAIM_TIER_REPORT.JSON');assert c['research_only'] and 'real_policy_value' in c['not_established'] and 'production_treatment_selection' in c['not_established']
def test_exposure_zero():
 e=load(ART/'GOLDEN_EXPOSURE_LEDGER.JSON');assert e['complete'] and e['protected_evidence_exposure']==0 and e['hidden_evaluation_queries']==0
def test_invariant_matrix_all_passed():
 m=load(ART/'INVARIANT_ACCEPTANCE_MATRIX.JSON');assert m['all_passed'] and all(x['passed'] for x in m['rows'])
@pytest.mark.parametrize('name',['MODEL_RISK_REVIEW.JSON','SECURITY_REVIEW.JSON','MUTATION_TEST_MATRIX.JSON','FUTURE_SUFFIX_INVARIANCE_REPORT.JSON','BASELINE_PRESERVATION_MATRIX.JSON','OBJECTIVE_FREEZE_RECORD.JSON'])
def test_review_artifact_exists(name):assert (ART/name).is_file() and load(ART/name)
