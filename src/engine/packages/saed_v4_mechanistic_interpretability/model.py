from __future__ import annotations
import math
from typing import Any
from .numerics import dot, sigmoid

def forward(record:dict[str,Any], *, features=None, views=None, transfer=True, adaptation=True, calibration=True, interactions=True, layer1_override=None, layer2_override=None, feature_weights=None) -> dict[str,Any]:
    x=list(record["feature_values"] if features is None else features)
    v=list(record["view_values"] if views is None else views)
    fw=list(record["feature_weights"] if feature_weights is None else feature_weights)
    m1,m2=record["layer_matrices"]
    layer1=[math.tanh(dot(row,x)+0.15*dot(record["view_weights"],v)+0.05*dot(fw,x)) for row in m1]
    if layer1_override is not None: layer1=list(layer1_override)
    layer2=[math.tanh(dot(row,layer1)) for row in m2]
    if layer2_override is not None: layer2=list(layer2_override)
    terms={
      "representation":dot(record["output_weights"],layer2),
      "transfer":sum(s["weight"]*s["source_score"] for s in record["transfer_sources"])*0.12 if transfer else 0.0,
      "adaptation":dot(record["adaptation_deltas"],x) if adaptation else 0.0,
      "calibration":dot(record["calibration_components"],record["calibration_weights"]) if calibration else 0.0,
      "treatment_interaction":sum(i["weight"]*x[record["feature_names"].index(i["left_feature"])]*x[record["feature_names"].index(i["right_feature"])] for i in record["treatment_interactions"]) if interactions else 0.0,
    }
    logit=float(record["bias"])+sum(terms.values())
    return {"layer1":layer1,"layer2":layer2,"terms":terms,"logit":logit,"score":sigmoid(logit)}
