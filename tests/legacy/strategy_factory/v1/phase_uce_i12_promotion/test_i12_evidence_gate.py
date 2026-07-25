from dataclasses import replace
from strategy_factory_promotion_v3.calibration import build_calibration_report
from strategy_factory_promotion_v3.canonical import canonical_sha256
from strategy_factory_promotion_v3.contracts import TestEvidence
from strategy_factory_promotion_v3.evidence import *
from strategy_factory_promotion_v3.enums import DecisionRole,EvidenceStatus,GateOutcome,NullKind,Severity,StressKind
from strategy_factory_promotion_v3.gate import decide
from strategy_factory_promotion_v3.golden import *
from strategy_factory_promotion_v3.multiplicity import multiplicity_report
from strategy_factory_promotion_v3.nulls import evaluate_null
from strategy_factory_promotion_v3.scorecard import build_scorecard
from strategy_factory_promotion_v3.stress import evaluate_stress
from strategy_factory_promotion_v3.uncertainty import build_uncertainty_report

def fixtures():
    u=golden_universe(); p=golden_policy(); unc=build_uncertainty_report(golden_returns(),report_name='gate',iterations=200); mult=multiplicity_report(u,golden_family_definition()); score=build_scorecard(golden_test_evidence()); n=80
    nulls=[evaluate_null(k,golden_returns(n),golden_baseline(n),iterations=300,seed=7+i) for i,k in enumerate(p.mandatory_nulls)]
    stresses=[evaluate_stress(StressKind.COST,golden_returns(n),[x-.005 for x in golden_returns(n)],minimum_retention=.5)]
    cal=build_calibration_report(golden_labels(n),golden_probabilities(n),conformal_lower=[0]*n,conformal_upper=[1]*n,conformal_observed=golden_labels(n),target_coverage=.95,outcomes=golden_returns(n),risk_tiers=['low' if i%2 else 'high' for i in range(n)])
    artifacts={'uncertainty':unc.evidence_hash,'multiplicity':mult.evidence_hash,'scorecard':score.evidence_hash,'calibration':cal.evidence_hash}
    bundle=sign_bundle(build_bundle(candidate_key='uce.candidate.golden',universe_hash=u.universe_hash,policy_hash=p.policy_hash,artifact_hashes=artifacts,generated_known_time_ms=1800000000001,signer_key_id='test.key'),b'secret')
    return u,p,unc,mult,score,nulls,stresses,cal,bundle

def test_bundle_signature_verifies():
    *_,bundle=fixtures(); assert verify_bundle(bundle,b'secret')
def test_tampered_bundle_signature_fails():
    *_,bundle=fixtures(); assert not verify_bundle(replace(bundle,candidate_key='other'),b'secret')
def test_artifact_integrity_detects_mismatch():
    *_,bundle=fixtures(); actual=dict(bundle.artifact_hashes); actual['uncertainty']='0'*64; assert not artifact_integrity(bundle,actual)['passed']
def test_clean_gate_promotes():
    u,p,unc,mult,score,nulls,stresses,cal,bundle=fixtures(); d=decide(candidate_key='uce.candidate.golden',role=DecisionRole.PROSPECTIVE_CHALLENGE,universe=u,policy=p,scorecard=score,uncertainty=unc,multiplicity=mult,pbo=.1,deflated_probability=.98,reality_check_p=.01,null_results=nulls,stress_results=stresses,calibration=cal,prospective_freeze=golden_freeze(),evidence_bundle=bundle,signing_secret=b'secret'); assert d.outcome is GateOutcome.PROMOTE
def test_critical_blocker_cannot_be_averaged_away():
    evidence=list(golden_test_evidence()); evidence[-1]=replace(evidence[-1],status=EvidenceStatus.FAIL,blockers=('known_time_leakage',)); score=build_scorecard(evidence); u,p,unc,mult,_,nulls,stresses,cal,bundle=fixtures(); d=decide(candidate_key='uce.candidate.golden',role=DecisionRole.CONFIRMATION,universe=u,policy=p,scorecard=score,uncertainty=unc,multiplicity=mult,pbo=.01,deflated_probability=.999,reality_check_p=.001,null_results=nulls,stress_results=stresses,calibration=cal,prospective_freeze=golden_freeze(),evidence_bundle=bundle,signing_secret=b'secret'); assert d.outcome is GateOutcome.REJECT and 'known_time_leakage' in d.blockers
def test_missing_mandatory_null_rejects():
    u,p,unc,mult,score,nulls,stresses,cal,bundle=fixtures(); d=decide(candidate_key='uce.candidate.golden',role=DecisionRole.CONFIRMATION,universe=u,policy=p,scorecard=score,uncertainty=unc,multiplicity=mult,pbo=.1,deflated_probability=.98,reality_check_p=.01,null_results=nulls[:-1],stress_results=stresses,calibration=cal,prospective_freeze=golden_freeze(),evidence_bundle=bundle,signing_secret=b'secret'); assert d.outcome is GateOutcome.REJECT
def test_bad_signature_rejects():
    u,p,unc,mult,score,nulls,stresses,cal,bundle=fixtures(); d=decide(candidate_key='uce.candidate.golden',role=DecisionRole.CONFIRMATION,universe=u,policy=p,scorecard=score,uncertainty=unc,multiplicity=mult,pbo=.1,deflated_probability=.98,reality_check_p=.01,null_results=nulls,stress_results=stresses,calibration=cal,prospective_freeze=golden_freeze(),evidence_bundle=bundle,signing_secret=b'wrong'); assert 'evidence_signature_invalid' in d.blockers
def test_noncritical_calibration_issue_challenges_not_promotes():
    u,p,unc,mult,score,nulls,stresses,cal,bundle=fixtures(); cal=replace(cal,expected_calibration_error=.2); d=decide(candidate_key='uce.candidate.golden',role=DecisionRole.CONFIRMATION,universe=u,policy=p,scorecard=score,uncertainty=unc,multiplicity=mult,pbo=.1,deflated_probability=.98,reality_check_p=.01,null_results=nulls,stress_results=stresses,calibration=cal,prospective_freeze=golden_freeze(),evidence_bundle=bundle,signing_secret=b'secret'); assert d.outcome is GateOutcome.CHALLENGE
