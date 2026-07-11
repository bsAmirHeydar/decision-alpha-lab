from strategy_factory_validation import *

def rows():
 return tuple(FoldObservation(f"o{i}","t","p","f",FoldRole.TEST,f"e{i}",f"c{i}",f"u{i}",i,i+1,x,x+0.02,0.02).with_hash() for i,x in enumerate((1.0,0.2,0.1,-0.1)))

def test_best_trade_removal_changes_mean():
 s=StressScenario("best","1",StressKind.BEST_TRADE_REMOVAL,remove_best_count=1).with_hash();r=evaluate_stress("t",rows(),s);assert r.sample_count==3;assert r.mean_net_r<0.3

def test_failed_gate_has_explicit_reason():
 e=PromotionEvidence(2,20,0.4,-0.5,0.1,0.8,0.5,0.5,0.1,-0.2,-0.2,1);d=evaluate_promotion("d","p","t",e);assert d.status==PromotionStatus.REJECTED;assert "LEAKAGE_DETECTED" in d.rejection_reasons

def test_strong_evidence_only_reaches_dataset_review():
 e=PromotionEvidence(6,200,0.8,0.02,0.7,0.2,0.99,0.01,0.7,0.03,0.01,0);d=evaluate_promotion("d","p","t",e);assert d.status==PromotionStatus.ELIGIBLE_FOR_DATASET_REVIEW
