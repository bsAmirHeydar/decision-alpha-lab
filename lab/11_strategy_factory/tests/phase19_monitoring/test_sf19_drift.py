from strategy_factory_monitoring import *

def test_stable_distribution_is_not_critical():
    r=evaluate_drift(reference_baseline(),reference_observation(False),reference_drift_policy());assert r.sufficient_samples;assert r.severity in {Severity.INFO,Severity.WARNING};assert r.psi<.05

def test_shifted_distribution_is_critical():
    r=evaluate_drift(reference_baseline(),reference_observation(True),reference_drift_policy());assert r.severity==Severity.CRITICAL;assert r.psi>.25

def test_prediction_lineage_is_exact():
    b=reference_baseline(DriftKind.PREDICTION);o=reference_observation(False,DriftKind.PREDICTION);p=reference_drift_policy(DriftKind.PREDICTION);assert evaluate_drift(b,o,p).kind==DriftKind.PREDICTION

def test_execution_mismatch_is_critical():
    o=ExecutionDriftObservation("o",1,2,100,90,2,2,1,2,1000,2000,0);r=evaluate_execution_drift(o,reference_execution_policy());assert r.severity==Severity.CRITICAL

def test_execution_low_sample_is_info():
    o=ExecutionDriftObservation("o",1,2,2,2,0,0,0,0,1,1,0);r=evaluate_execution_drift(o,reference_execution_policy());assert r.severity==Severity.INFO;assert not r.sufficient_samples
