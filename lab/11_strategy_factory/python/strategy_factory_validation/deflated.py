from __future__ import annotations
from statistics import NormalDist
import math
from .models import DeflatedPerformanceResult
from .hashing import stable_id

def deflated_sharpe_probability(trial_id: str, observed_sharpe: float,
                                number_of_trials: int, sample_count: int,
                                skewness: float = 0.0,
                                kurtosis: float = 3.0,
                                sharpe_variance: float | None = None) -> DeflatedPerformanceResult:
    if not trial_id or number_of_trials < 1 or sample_count < 3:
        raise ValueError("invalid deflated-performance inputs")
    if kurtosis < 1.0:
        raise ValueError("kurtosis must be at least one")
    nd=NormalDist(); gamma=0.5772156649015329
    variance = (1.0 / max(1, sample_count - 1) if sharpe_variance is None
                else sharpe_variance)
    variance=max(variance,1e-15)
    if number_of_trials == 1:
        expected_max=0.0
    else:
        p1=max(1e-12,min(1-1e-12,1.0-1.0/number_of_trials))
        p2=max(1e-12,min(1-1e-12,1.0-1.0/(number_of_trials*math.e)))
        expected_max=math.sqrt(variance)*((1-gamma)*nd.inv_cdf(p1)+gamma*nd.inv_cdf(p2))
    denominator=math.sqrt(max(1e-15,1.0-skewness*observed_sharpe+
                              ((kurtosis-1.0)/4.0)*observed_sharpe**2))
    z=(observed_sharpe-expected_max)*math.sqrt(sample_count-1)/denominator
    probability=nd.cdf(z)
    payload=f"{trial_id}|{observed_sharpe}|{expected_max}|{probability}|{number_of_trials}|{sample_count}|{skewness}|{kurtosis}"
    return DeflatedPerformanceResult(trial_id,observed_sharpe,expected_max,
        probability,number_of_trials,sample_count,skewness,kurtosis,
        stable_id("dsr",payload))
