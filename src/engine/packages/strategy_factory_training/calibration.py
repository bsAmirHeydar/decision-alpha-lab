from __future__ import annotations
import math
from .enums import CalibrationMethod
from .models import CalibrationArtifact
from .baselines import sigmoid
from .hashing import sha256_lines

def fit_calibration(method:CalibrationMethod,raw_scores,labels,model_artifact_hash:str,row_hashes,
                    calibration_id:str="phase13_validation_calibration",iterations:int=300)->CalibrationArtifact:
    if len(raw_scores)!=len(labels) or not labels:raise ValueError("calibration inputs must be aligned and non-empty")
    intercept=0.0;slope=1.0
    if method==CalibrationMethod.PLATT:
        intercept=0.0;slope=0.0;n=len(labels)
        for step in range(iterations):
            gi=0.0;gs=0.0
            for score,target in zip(raw_scores,labels):
                error=sigmoid(intercept+slope*score)-target;gi+=error;gs+=error*score
            rate=0.05/(1+0.002*step);intercept-=rate*gi/n;slope-=rate*gs/n
    artifact=CalibrationArtifact(calibration_id=calibration_id,method=method,
        model_artifact_hash=model_artifact_hash,validation_rowset_hash=sha256_lines(row_hashes),
        intercept=intercept,slope=slope,sample_count=len(labels)).with_hash()
    return artifact

def apply_calibration(raw_score:float,artifact:CalibrationArtifact)->float:
    if artifact.method==CalibrationMethod.NONE:
        return sigmoid(raw_score)
    return sigmoid(artifact.intercept+artifact.slope*raw_score)
