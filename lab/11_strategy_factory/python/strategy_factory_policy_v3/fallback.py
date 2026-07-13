from __future__ import annotations
from .contracts import FallbackPolicy,ManualDecision
from .enums import FallbackReason,FallbackAction,DecisionStatus,Action,Authority

def default_fallback_policy()->FallbackPolicy:
    from .contracts import FallbackRule
    manual=(FallbackReason.INVALID_MODEL,FallbackReason.STALE_MODEL,FallbackReason.STALE_FEATURES,FallbackReason.OUT_OF_DISTRIBUTION,FallbackReason.LOW_CONFIDENCE,FallbackReason.TIMEOUT,FallbackReason.MISSING_VIEW,FallbackReason.SIGNATURE_FAILURE)
    rules=[FallbackRule(r,FallbackAction.MANUAL_ONLY,'preserve pinned manual doctrine') for r in manual]
    rules += [FallbackRule(FallbackReason.CONFLICT,FallbackAction.ABSTAIN),FallbackRule(FallbackReason.UNSUPPORTED_ACTION,FallbackAction.ABSTAIN),FallbackRule(FallbackReason.UNSUPPORTED_TREATMENT,FallbackAction.ABSTAIN),FallbackRule(FallbackReason.UNSUPPORTED_RISK,FallbackAction.ABSTAIN),FallbackRule(FallbackReason.RISK_REJECTION,FallbackAction.REJECT),FallbackRule(FallbackReason.KILL_SWITCH,FallbackAction.REJECT)]
    return FallbackPolicy('default_fallback','1.0.0',tuple(rules),FallbackAction.ABSTAIN)

def fallback_resolution(policy:FallbackPolicy,reason:FallbackReason,manual:ManualDecision):
    action=policy.action_for(reason)
    if action is FallbackAction.MANUAL_ONLY:
        if manual.eligible and not manual.vetoed:return DecisionStatus.APPROVED,manual.action,manual.treatment,manual.risk_tier,Authority.MANUAL_POLICY,action,('fallback_manual_only',reason.value)
        return DecisionStatus.INELIGIBLE,Action.NO_ACTION,None,None,Authority.MANUAL_POLICY,action,('fallback_manual_ineligible',reason.value)
    if action is FallbackAction.REJECT:return DecisionStatus.REJECTED,Action.REJECT,None,None,Authority.SYSTEM,action,('fallback_reject',reason.value)
    return DecisionStatus.ABSTAINED,Action.ABSTAIN,None,None,Authority.SYSTEM,action,('fallback_abstain',reason.value)
