from __future__ import annotations
from dataclasses import asdict
from .contracts import *
from .graph import CompiledGraph
from .manual import evaluate_manual
from .model import validate_model_output,argmax_stable
from .fallback import fallback_resolution
from .authority import resolve_hard_authority
from .evidence import append_trace,TraceEntry
from .enums import *
from .canonical import stable_id
from .errors import PolicyError

def execute_policy(graph:CompiledGraph,occurrence:ContextOccurrence,manual_policy:ManualPolicyDefinition,fallback_policy:FallbackPolicy,authority_matrix:AuthorityMatrix,*,admission:PromotionAdmission|None=None,model_output:ModelOutput|None=None,operator_override:OperatorOverride|None=None)->PolicyDecision:
    spec=graph.spec
    if spec.manual_policy_hash!=manual_policy.policy_hash or spec.fallback_policy_hash!=fallback_policy.policy_hash or spec.authority_matrix_hash!=authority_matrix.matrix_hash: raise PolicyError('policy_dependency_hash_mismatch','graph dependency hash mismatch')
    if occurrence.context_type not in spec.supported_context_types: raise PolicyError('graph_context_unsupported','occurrence context outside graph support')
    manual=evaluate_manual(manual_policy,occurrence); trace=[]; state={'status':DecisionStatus.APPROVED if manual.eligible else DecisionStatus.INELIGIBLE,'action':manual.action,'treatment':manual.treatment,'risk':manual.risk_tier,'score':None,'reason':None,'fallback':None,'authority':Authority.MANUAL_POLICY,'manual_veto':manual.vetoed,'risk_rejected':False,'kill_switch':False,'approval_required':False}
    nodes={n.node_id:n for n in spec.nodes}
    model_valid=False; model_reason=None; model_notes=()
    if model_output is not None and admission is not None:
        model_valid,model_reason,model_notes=validate_model_output(admission,occurrence,model_output)
    for node_id in graph.topological_order:
        node=nodes[node_id]; payload={}
        if node.kind is NodeKind.INPUT: payload={'occurrence_hash':occurrence.occurrence_hash}
        elif node.kind is NodeKind.MANUAL_ELIGIBILITY:
            payload={'eligible':manual.eligible,'vetoed':manual.vetoed}; state['status']=DecisionStatus.APPROVED if manual.eligible else DecisionStatus.INELIGIBLE
        elif node.kind is NodeKind.MANUAL_TREATMENT:
            state.update(action=manual.action,treatment=manual.treatment,risk=manual.risk_tier); payload={'action':manual.action.value,'treatment':manual.treatment,'risk_tier':manual.risk_tier}
        elif node.kind in (NodeKind.MODEL_FILTER,NodeKind.MODEL_RANK,NodeKind.MODEL_TREATMENT,NodeKind.MODEL_RISK):
            if model_output is None or admission is None or not model_valid:
                reason=model_reason or FallbackReason.INVALID_MODEL
                status,action,treatment,risk,auth,fb,reasons=fallback_resolution(fallback_policy,reason,manual)
                state.update(status=status,action=action,treatment=treatment,risk=risk,authority=auth,fallback=fb,reason=reason)
                payload={'fallback':fb.value,'reason':reason.value,'notes':model_notes}
            elif node.kind is NodeKind.MODEL_FILTER:
                action=str(node.config.get('action',manual.action.value)); p=model_output.action_probabilities.get(action,0.0); minp=float(node.config.get('minimum_probability',.5)); minu=float(node.config.get('minimum_utility',0.0))
                if p<minp or model_output.utility<minu:
                    state.update(status=DecisionStatus.ABSTAINED,action=Action.ABSTAIN,authority=Authority.MODEL,reason=FallbackReason.LOW_CONFIDENCE)
                else: state['score']=p
                payload={'probability':p,'minimum_probability':minp,'utility':model_output.utility,'passed':p>=minp and model_output.utility>=minu}
            elif node.kind is NodeKind.MODEL_RANK:
                state['score']=model_output.rank_score
                if model_output.rank_score<float(node.config.get('minimum_rank',0.0)): state.update(status=DecisionStatus.ABSTAINED,action=Action.ABSTAIN,authority=Authority.MODEL,reason=FallbackReason.LOW_CONFIDENCE)
                payload={'rank_score':model_output.rank_score}
            elif node.kind is NodeKind.MODEL_TREATMENT:
                choice=argmax_stable(model_output.treatment_distribution)
                if choice not in spec.supported_treatments or choice not in occurrence.available_treatments:
                    status,a,t,r,auth,fb,reasons=fallback_resolution(fallback_policy,FallbackReason.UNSUPPORTED_TREATMENT,manual); state.update(status=status,action=a,treatment=t,risk=r,authority=auth,fallback=fb,reason=FallbackReason.UNSUPPORTED_TREATMENT)
                else: state['treatment']=choice; state['authority']=Authority.MODEL
                payload={'treatment':choice}
            elif node.kind is NodeKind.MODEL_RISK:
                choice=argmax_stable(model_output.risk_distribution)
                if choice not in spec.supported_risk_tiers or choice not in occurrence.available_risk_tiers:
                    status,a,t,r,auth,fb,reasons=fallback_resolution(fallback_policy,FallbackReason.UNSUPPORTED_RISK,manual); state.update(status=status,action=a,treatment=t,risk=r,authority=auth,fallback=fb,reason=FallbackReason.UNSUPPORTED_RISK)
                else: state['risk']=choice; state['authority']=Authority.MODEL
                payload={'risk_tier':choice}
        elif node.kind is NodeKind.MANUAL_VETO: state['manual_veto']=manual.vetoed; payload={'vetoed':manual.vetoed}
        elif node.kind is NodeKind.OPERATOR_APPROVAL:
            state['approval_required']=bool(node.config.get('required',True)); payload={'required':state['approval_required'],'override':operator_override.kind.value if operator_override else None}
        elif node.kind is NodeKind.PORTFOLIO_ALLOCATION:
            if not bool(node.config.get('capacity_available',True)): state.update(status=DecisionStatus.ABSTAINED,action=Action.ABSTAIN,authority=Authority.PORTFOLIO_ENGINE,reason=FallbackReason.CONFLICT)
            payload={'capacity_available':bool(node.config.get('capacity_available',True)),'allocation_weight':float(node.config.get('allocation_weight',1.0))}
        elif node.kind is NodeKind.RISK_GATE: state['risk_rejected']=bool(node.config.get('risk_rejected',False)); payload={'risk_rejected':state['risk_rejected']}
        elif node.kind is NodeKind.KILL_SWITCH: state['kill_switch']=bool(node.config.get('engaged',False)); payload={'engaged':state['kill_switch']}
        elif node.kind is NodeKind.FALLBACK: payload={'active':state['fallback'].value if state['fallback'] else None}
        elif node.kind is NodeKind.OUTPUT:
            hard_status,hard_auth,hard_reasons=resolve_hard_authority(kill_switch=state['kill_switch'],risk_rejected=state['risk_rejected'],manual_veto=state['manual_veto'],override=operator_override,known_time_ms=occurrence.known_time_ms)
            if hard_auth is not None and (hard_status is DecisionStatus.REJECTED or state['approval_required'] or operator_override is not None): state.update(status=hard_status,authority=hard_auth)
            elif state['approval_required'] and operator_override is None and state['status'] is DecisionStatus.APPROVED: state['status']=DecisionStatus.PENDING_APPROVAL
            if state['status'] in (DecisionStatus.REJECTED,DecisionStatus.ABSTAINED,DecisionStatus.INELIGIBLE,DecisionStatus.PENDING_APPROVAL) and state['action'] not in (Action.REJECT,Action.ABSTAIN,Action.NO_ACTION):
                state['action']={DecisionStatus.REJECTED:Action.REJECT,DecisionStatus.ABSTAINED:Action.ABSTAIN,DecisionStatus.INELIGIBLE:Action.NO_ACTION,DecisionStatus.PENDING_APPROVAL:state['action']}[state['status']]
            payload={'status':state['status'].value,'action':state['action'].value,'decisive_authority':state['authority'].value,'hard_reasons':hard_reasons}
        append_trace(trace,node.node_id,node.kind.value,state['status'].value,payload)
    reasons=list(manual.reasons)
    if state['reason'] is not None: reasons.append(state['reason'].value)
    decision_payload={'occurrence':occurrence.occurrence_hash,'graph':spec.graph_hash,'manual':manual.decision_hash,'model':model_output.output_hash if model_output else None,'status':state['status'].value,'action':state['action'].value,'treatment':state['treatment'],'risk':state['risk'],'trace_tail':trace[-1].entry_hash}
    return PolicyDecision(stable_id('policy_decision',decision_payload),occurrence.occurrence_id,state['status'],state['action'],state['treatment'],state['risk'],state['score'],tuple(reasons),tuple({'sequence':e.sequence,'node_id':e.node_id,'node_kind':e.node_kind,'status':e.status,'payload':dict(e.payload),'previous_hash':e.previous_hash,'entry_hash':e.entry_hash} for e in trace),state['fallback'],state['authority'],spec.graph_hash,manual.decision_hash,model_output.output_hash if model_output else None,occurrence.known_time_ms)
