from __future__ import annotations
from .contracts import AuthorityMatrix,OperatorOverride
from .enums import Authority,OverrideKind,DecisionStatus,FallbackReason
from .errors import PolicyError

def default_authority_matrix()->AuthorityMatrix:
    from .contracts import AuthorityRule
    from .enums import ConflictDisposition
    precedence=(Authority.KILL_SWITCH,Authority.RISK_ENGINE,Authority.HUMAN_OPERATOR,Authority.MANUAL_POLICY,Authority.TREATMENT_COMPILER,Authority.MODEL,Authority.PORTFOLIO_ENGINE,Authority.SYSTEM)
    rules=(
      AuthorityRule('kill_switch_over_all',Authority.KILL_SWITCH,tuple(a for a in Authority if a is not Authority.KILL_SWITCH),ConflictDisposition.ACCEPT_HIGHER_AUTHORITY,True),
      AuthorityRule('risk_reject_over_approval',Authority.RISK_ENGINE,(Authority.HUMAN_OPERATOR,Authority.MANUAL_POLICY,Authority.MODEL),ConflictDisposition.ACCEPT_HIGHER_AUTHORITY,True),
      AuthorityRule('operator_veto_over_model',Authority.HUMAN_OPERATOR,(Authority.MODEL,),ConflictDisposition.ACCEPT_HIGHER_AUTHORITY,True),
      AuthorityRule('manual_support_bounds_model',Authority.MANUAL_POLICY,(Authority.MODEL,),ConflictDisposition.ACCEPT_HIGHER_AUTHORITY,True),)
    return AuthorityMatrix('default_authority','1.0.0',rules,precedence)

def resolve_hard_authority(*,kill_switch:bool,risk_rejected:bool,manual_veto:bool,override:OperatorOverride|None,known_time_ms:int)->tuple[DecisionStatus,Authority|None,tuple[str,...]]:
    if kill_switch:return DecisionStatus.REJECTED,Authority.KILL_SWITCH,('kill_switch_engaged',)
    if risk_rejected:return DecisionStatus.REJECTED,Authority.RISK_ENGINE,('risk_engine_rejected',)
    if manual_veto:return DecisionStatus.REJECTED,Authority.MANUAL_POLICY,('manual_policy_veto',)
    if override is not None:
        if not override.issued_at_ms<=known_time_ms<=override.expires_at_ms: raise PolicyError('override_outside_validity','operator override expired or not yet valid')
        if override.kind is OverrideKind.VETO:return DecisionStatus.REJECTED,Authority.HUMAN_OPERATOR,('operator_veto',)
        return DecisionStatus.APPROVED,Authority.HUMAN_OPERATOR,('operator_approval',)
    return DecisionStatus.PENDING_APPROVAL,None,()
