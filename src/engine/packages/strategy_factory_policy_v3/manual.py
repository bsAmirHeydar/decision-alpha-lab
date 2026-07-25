from __future__ import annotations
from .contracts import *
from .predicates import all_match,any_match
from .enums import Action
from .errors import PolicyError

def _payload(occurrence:ContextOccurrence):
    return {'context_type':occurrence.context_type,'known_time_ms':occurrence.known_time_ms,'feature_time_ms':occurrence.feature_time_ms,'features':dict(occurrence.features),'metadata':dict(occurrence.metadata),'views_present':occurrence.views_present}

def evaluate_manual(policy:ManualPolicyDefinition,occurrence:ContextOccurrence)->ManualDecision:
    if occurrence.context_type!=policy.context_type:
        return ManualDecision(False,Action.NO_ACTION,None,None,False,(),('context_type_mismatch',),policy.policy_hash)
    if not policy.valid_from_ms<=occurrence.known_time_ms<=policy.valid_until_ms:
        return ManualDecision(False,Action.NO_ACTION,None,None,False,(),('manual_policy_outside_validity',),policy.policy_hash)
    payload=_payload(occurrence)
    eligible=all_match(policy.eligibility,payload)
    if not eligible:return ManualDecision(False,Action.NO_ACTION,None,None,False,(),('manual_eligibility_failed',),policy.policy_hash)
    if any_match(policy.vetoes,payload):return ManualDecision(False,Action.REJECT,None,None,True,(),('manual_veto',),policy.policy_hash)
    action,treatment,risk=policy.action,policy.treatment,policy.risk_tier; matched=[]
    for rule in policy.exceptions:
        if all_match(rule.when,payload):
            matched.append(rule.rule_id)
            if rule.veto:return ManualDecision(False,Action.REJECT,None,None,True,tuple(matched),('manual_exception_veto',rule.rule_id),policy.policy_hash)
            action=rule.action or action; treatment=rule.treatment or treatment; risk=rule.risk_tier or risk
    if action.value not in occurrence.candidate_actions: raise PolicyError('manual_action_unsupported','manual action outside occurrence support')
    if treatment not in occurrence.available_treatments: raise PolicyError('manual_treatment_unsupported','manual treatment outside occurrence support')
    if risk not in occurrence.available_risk_tiers: raise PolicyError('manual_risk_unsupported','manual risk outside occurrence support')
    return ManualDecision(True,action,treatment,risk,False,tuple(matched),('manual_policy_matched',),policy.policy_hash)


def manual_projection(decision:ManualDecision)->dict:
    """Canonical semantic projection used by manual-only parity certification."""
    return {'eligible':decision.eligible,'action':decision.action.value,'treatment':decision.treatment,'risk_tier':decision.risk_tier,'vetoed':decision.vetoed,'matched_exceptions':list(decision.matched_exceptions),'reasons':list(decision.reasons),'policy_hash':decision.policy_hash}

def policy_decision_manual_projection(decision)->dict:
    return {'eligible':decision.status.value=='approved','action':decision.action.value,'treatment':decision.treatment,'risk_tier':decision.risk_tier,'vetoed':decision.status.value=='rejected' and decision.decisive_authority.value=='manual_policy','matched_exceptions':[],'reasons':list(decision.reasons),'policy_hash':decision.manual_decision_hash}
