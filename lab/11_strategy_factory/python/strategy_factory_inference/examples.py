from __future__ import annotations
from .models import *
from .enums import *
from .preprocessing import transform
from .reference import linear_score,calibrate,classify

FEATURES=(
 FeatureBinding("ref.range_position","1.0.0",0),
 FeatureBinding("ref.body_fraction","1.0.0",1),
 FeatureBinding("ref.displacement_atr","1.0.0",2),
 FeatureBinding("ref.session_progress","1.0.0",3),
)
FEATURE_SCHEMA_HASH="fvec_b0f3a1edd021edee"
FEATURE_ORDER=FeatureOrder(FEATURE_SCHEMA_HASH,FEATURES).with_hash()
PREPROCESSING=PreprocessingManifest(FEATURE_SCHEMA_HASH,"xform_bb9fb122fd545bcc",(0.0,0.0,0.0,0.5),(0.1,-0.2,0.3,0.5),(1.2,0.8,2.0,0.25),fitted_rowset_hash="rowset_reference_phase15").with_hash()
CALIBRATION=CalibrationContract(CalibrationMethod.SIGMOID,1.0,0.0,0.55).with_hash()
INPUT=TensorContract("features",TensorElementType.FLOAT32,(1,4)).with_hash()
OUTPUT=TensorContract("score",TensorElementType.FLOAT32,(1,1)).with_hash()
WEIGHTS=(0.75,-0.5,0.25,1.1); BIAS=-0.15

def make_vectors():
 rows=[
  ((0.1,-0.2,0.3,0.5),(False,False,False,False)),
  ((0.9,0.4,1.5,0.8),(False,False,False,False)),
  ((-0.4,-0.8,-1.0,0.2),(False,False,False,False)),
  ((0.0,0.0,0.0,0.0),(True,True,True,True)),
  ((0.6,0.1,0.0,0.75),(False,True,False,False)),
  ((-1.2,1.0,2.5,0.1),(False,False,True,False)),
  ((2.0,-1.5,0.75,1.0),(False,False,False,False)),
  ((0.05,-0.1,0.25,0.48),(False,False,False,False)),
 ]
 out=[]
 for idx,(values,missing) in enumerate(rows):
  transformed=transform(values,missing,PREPROCESSING); raw=linear_score(transformed,WEIGHTS,BIAS); cal=calibrate(raw,CALIBRATION)
  out.append(ParityVector(f"pv{idx+1:03d}",tuple(values),tuple(missing),transformed,raw,cal,classify(cal,CALIBRATION.threshold)).with_hash())
 return tuple(out)
