from __future__ import annotations
from .canonical import content_hash, stable_id
from .errors import EvaluationError
from .feature_space import flatten_multimodal_features, compare

def _rule_matches(rule:dict,features:dict)->tuple[bool,list[dict]]:
    checks=[]
    for p in rule['predicates']:
        present=p['feature_ref'] in features and features[p['feature_ref']] is not None
        if not present and p.get('missing_policy','fail_rule')=='fail_program': raise EvaluationError(f"missing required feature: {p['feature_ref']}")
        if not present:
            matched=p.get('missing_policy')=='match_only_missing'
        else:
            matched=compare(features[p['feature_ref']],p['operator'],p.get('expected'))
        checks.append({"feature_ref":p['feature_ref'],"operator":p['operator'],"expected":p.get('expected'),"actual":features.get(p['feature_ref']),"present":present,"matched":matched})
        if not matched: return False,checks
    return True,checks

def evaluate_program(compiled:dict,view_package:dict)->dict:
    features=flatten_multimodal_features(view_package)
    evaluated=[]; selected=compiled['fallback_node_id']; matched_rule=None; reason='fallback_abstain'
    for rule in compiled['rules']:
        matched,checks=_rule_matches(rule,features)
        evaluated.append({"rule_id":rule['rule_id'],"priority":rule['priority'],"matched":matched,"checks":checks})
        if matched:
            selected=rule['action_node_id']; matched_rule=rule['rule_id']; reason=rule['reason_code']; break
    payload={"phase":"SAED_V4_10","compiled_program_id":compiled['compiled_program_id'],"compiled_program_hash":compiled['compiled_program_hash'],"source_view_package_hash":view_package['package_hash'],"decision_time":view_package['event_as_of'],"known_as_of":view_package['known_as_of'],"matched_rule_id":matched_rule,"projected_node_id":selected,"reason_code":reason,"rule_evaluations":evaluated,"trace_semantics":"descriptive_manual_projection_only","selection_authority":False,"execution_authority":False}
    payload['trace_id']=stable_id('manualtrace',payload); payload['trace_hash']=content_hash(payload)
    return payload
