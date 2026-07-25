"""Deterministic golden fixtures spanning the complete I11-to-I12 handoff."""
from __future__ import annotations
from .canonical import canonical_sha256
from .contracts import FamilyDefinition, PromotionPolicy, ProspectiveChallengeFreeze, SelectionUniverse, TestEvidence, TrialEvidence
from .enums import CorrectionMethod, EvidenceStatus, Severity, TrialDisposition

def h(label:str)->str:return canonical_sha256({"golden":label})

def golden_trials()->tuple[TrialEvidence,...]:
    dispositions=(TrialDisposition.ATTEMPTED,TrialDisposition.FAILED,TrialDisposition.PRUNED,TrialDisposition.SKIPPED,TrialDisposition.INVALID,TrialDisposition.TIMED_OUT,TrialDisposition.CANCELLED,TrialDisposition.SELECTED,TrialDisposition.ENSEMBLED)
    rows=[]
    pvals=(.001,None,None,None,None,None,None,.002,.004)
    scores=(1.2,None,None,None,None,None,None,1.1,1.05)
    for i,(d,p,s) in enumerate(zip(dispositions,pvals,scores)):
        rows.append(TrialEvidence(trial_id=f"trial_{i:02d}",family_id="golden_family",candidate_key="uce.candidate.golden",task_key="classification",trainer_key="trainer.golden",treatment_key="treatment.base" if i<7 else "treatment.selected",threshold_key="threshold.default",disposition=d,ledger_entry_hash=h(f"ledger-{i}"),p_value=p,score=s,fold_id=f"wf_{i%3:02d}",seed=i,selected=d in (TrialDisposition.SELECTED,TrialDisposition.ENSEMBLED),ensembled=d is TrialDisposition.ENSEMBLED,metadata={"attempt_index":i}))
    return tuple(rows)

def golden_universe()->SelectionUniverse:
    trials=golden_trials()
    return SelectionUniverse(universe_id="uce_i12_golden_universe",universe_version="1.0.0",experiment_manifest_hash=h("manifest"),selection_ledger_hash=h("ledger"),dataset_hash=h("dataset"),split_hash=h("split"),target_hash=h("target"),economics_hash=h("economics"),known_time_hash=h("known-time"),trials=trials,declared_trial_count=len(trials),ledger_complete=True)

def golden_family_definition()->FamilyDefinition:
    return FamilyDefinition(family_definition_id="uce_i12_all_search_axes",dimensions=("family_id","task_key","trainer_key","treatment_key","threshold_key"),correction=CorrectionMethod.BENJAMINI_YEKUTIELY,alpha=.05,include_missing_p_values=True)

def golden_policy()->PromotionPolicy:
    return PromotionPolicy(policy_id="uce_i12_golden_policy",policy_version="1.0.0",alpha=.05,minimum_score=.75,minimum_effective_sample_size=8.0,maximum_pbo=.35,minimum_deflated_probability=.80,maximum_reality_check_p=.10,minimum_stress_retention=.55,maximum_ece=.12,coverage_tolerance=.08)

def golden_freeze()->ProspectiveChallengeFreeze:
    return ProspectiveChallengeFreeze(challenge_id="uce_i12_golden_prospective",challenge_version="1.0.0",declaration_hash=h("prospective-declaration"),frozen_before_observation=True,start_known_time_ms=1_800_000_000_000,end_known_time_ms=1_900_000_000_000,required_sample_count=100,decision_rule_hash=h("prospective-rule"))

def golden_test_evidence()->tuple[TestEvidence,...]:
    families=("uncertainty","multiplicity","winner_overfit","null_controls","stress","calibration","integrity")
    return tuple(TestEvidence(test_id=f"golden_{family}",family=family,status=EvidenceStatus.PASS,severity=Severity.CRITICAL if family in {"multiplicity","integrity"} else Severity.HIGH,metric_name=f"{family}_score",metric_value=.95,threshold=.80,evidence_hash=h(f"test-{family}")) for family in families)

def golden_returns(n:int=120)->tuple[float,...]:
    return tuple(0.18 + ((i%7)-3)*0.015 + (0.03 if i%11==0 else 0.0) for i in range(n))
def golden_baseline(n:int=120)->tuple[float,...]: return tuple(0.02 + ((i%5)-2)*0.01 for i in range(n))
def golden_probabilities(n:int=120)->tuple[float,...]: return tuple(.92 if i%3 else .08 for i in range(n))
def golden_labels(n:int=120)->tuple[int,...]: return tuple(0 if i%3==0 else 1 for i in range(n))
