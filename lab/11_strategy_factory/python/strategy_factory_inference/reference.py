from __future__ import annotations
import math
from .enums import CalibrationMethod
from .models import CalibrationContract

def linear_score(transformed, weights, bias: float) -> float:
    if len(transformed)!=len(weights): raise ValueError("linear width mismatch")
    score=float(bias)+sum(float(x)*float(w) for x,w in zip(transformed,weights))
    if not math.isfinite(score): raise ValueError("non-finite raw score")
    return score

def calibrate(raw_score: float, contract: CalibrationContract) -> float:
    contract.validate()
    if contract.method==CalibrationMethod.IDENTITY: value=raw_score
    elif contract.method in (CalibrationMethod.SIGMOID,CalibrationMethod.PLATT):
        z=contract.a*raw_score+contract.b
        value=0.0 if z<-745 else 1.0 if z>745 else 1.0/(1.0+math.exp(-z))
    else: raise ValueError("unsupported calibration")
    if not math.isfinite(value): raise ValueError("non-finite calibration output")
    return value

def classify(calibrated: float, threshold: float) -> int: return 1 if calibrated>=threshold else 0
