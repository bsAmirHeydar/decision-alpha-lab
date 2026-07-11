from __future__ import annotations
import math
from .models import ConfidenceInterval
from .enums import IntervalKind

def normal_mean_interval(metric_id: str, group_key: str, estimate: float, standard_deviation: float,
                         sample_count: int, confidence_level: float = .95) -> ConfidenceInterval:
    if sample_count < 1: raise ValueError("sample_count must be positive")
    if confidence_level != .95: raise ValueError("reference implementation currently freezes confidence at 0.95")
    se = standard_deviation / math.sqrt(sample_count) if sample_count > 1 else 0.0
    z = 1.959963984540054
    return ConfidenceInterval(metric_id, group_key, IntervalKind.NORMAL_MEAN, confidence_level,
                              estimate, estimate-z*se, estimate+z*se, se, sample_count).with_hash()

def wilson_interval(metric_id: str, group_key: str, successes: int, trials: int,
                    confidence_level: float = .95) -> ConfidenceInterval:
    if trials <= 0 or not 0 <= successes <= trials: raise ValueError("invalid binomial counts")
    if confidence_level != .95: raise ValueError("reference implementation currently freezes confidence at 0.95")
    z=1.959963984540054; p=successes/trials; z2=z*z
    center=(p+z2/(2*trials))/(1+z2/trials)
    half=z*math.sqrt((p*(1-p)+z2/(4*trials))/trials)/(1+z2/trials)
    se=math.sqrt(p*(1-p)/trials)
    return ConfidenceInterval(metric_id, group_key, IntervalKind.WILSON_PROPORTION,
                              confidence_level,p,max(0.0,center-half),min(1.0,center+half),se,trials).with_hash()
