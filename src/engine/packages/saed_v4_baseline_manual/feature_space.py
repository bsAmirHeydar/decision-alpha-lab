from __future__ import annotations
from typing import Any
from .errors import ContractError, LeakageError

FORBIDDEN_TOKENS={
 "outcome","net_r","gross_r","mfe","mae","exit_price","exit_reason","holding_ms",
 "fill_fraction","fill_probability","adjusted_net_r","future","label","target_value",
 "protected_final","prospective","shadow","live"
}
ALLOWED_OPERATORS={"eq","ne","gt","ge","lt","le","in","not_in","exists","missing"}

def flatten_multimodal_features(package: dict) -> dict[str,Any]:
    result={}
    for view in package.get('views',[]):
        view_name=view['view_name']
        for feature in view.get('features',[]):
            key=f"{view_name}:{feature['feature_id']}"
            result[key]=feature.get('value')
    return result

def feature_registry(package: dict) -> dict:
    features=[]
    for view in package.get('views',[]):
        for f in view.get('features',[]):
            ref=f"{view['view_name']}:{f['feature_id']}"
            features.append({
                "feature_ref":ref,"view_name":view['view_name'],"feature_id":f['feature_id'],
                "event_as_of":view['event_as_of'],"known_as_of":view['known_as_of'],
                "missing":bool(f.get('missing',False)),"stale":bool(f.get('stale',False)),
                "quality":float(f.get('quality',0.0)),"source_value_hashes":list(f.get('source_value_hashes',[]))
            })
    features.sort(key=lambda x:x['feature_ref'])
    return {"feature_count":len(features),"features":features,"known_as_of":package['known_as_of'],"event_as_of":package['event_as_of']}

def validate_feature_ref(ref: str, registry: dict) -> None:
    low=ref.lower()
    if any(token in low for token in FORBIDDEN_TOKENS): raise LeakageError(f"forbidden feature token: {ref}")
    known={x['feature_ref'] for x in registry['features']}
    if ref not in known: raise ContractError(f"unknown feature_ref: {ref}")

def compare(actual: Any, operator: str, expected: Any) -> bool:
    if operator not in ALLOWED_OPERATORS: raise ContractError(f"unknown operator: {operator}")
    if operator=='exists': return actual is not None
    if operator=='missing': return actual is None
    if operator=='eq': return actual==expected
    if operator=='ne': return actual!=expected
    if operator=='gt': return actual>expected
    if operator=='ge': return actual>=expected
    if operator=='lt': return actual<expected
    if operator=='le': return actual<=expected
    if operator=='in': return actual in expected
    if operator=='not_in': return actual not in expected
    raise AssertionError(operator)
