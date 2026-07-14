from __future__ import annotations
from .enums import FeatureType
from .errors import ViewBuildError

def validate_feature_value(defn,value):
    if value is None:return
    t=defn.feature_type
    if t==FeatureType.NUMBER and (not isinstance(value,(int,float)) or isinstance(value,bool)):raise ViewBuildError('number feature type mismatch')
    if t in {FeatureType.STRING,FeatureType.CATEGORY} and not isinstance(value,str):raise ViewBuildError('string feature type mismatch')
    if t==FeatureType.BOOLEAN and not isinstance(value,bool):raise ViewBuildError('boolean feature type mismatch')
    if t==FeatureType.VECTOR:
        if not isinstance(value,(list,tuple)):raise ViewBuildError('vector feature type mismatch')
        if defn.vector_length is not None and len(value)!=defn.vector_length:raise ViewBuildError('vector length mismatch')
    if defn.allowed_categories and value not in defn.allowed_categories:raise ViewBuildError('category outside allowlist')
    if isinstance(value,(int,float)) and not isinstance(value,bool):
        if defn.minimum is not None and value<defn.minimum:raise ViewBuildError('value below minimum')
        if defn.maximum is not None and value>defn.maximum:raise ViewBuildError('value above maximum')
