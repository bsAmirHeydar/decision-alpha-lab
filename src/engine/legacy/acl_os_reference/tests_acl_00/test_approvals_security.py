from __future__ import annotations
from dataclasses import replace
from datetime import timedelta
from src.engine.tooling.strategy_factory.acl_os.acl_00.approvals import ApprovalEvaluator
from src.engine.tooling.strategy_factory.acl_os.acl_00.canonical import StructuralSignatureVerifier
from src.engine.tooling.strategy_factory.acl_os.acl_00.security import SecurityHookEvaluator
from src.engine.tooling.strategy_factory.acl_os.acl_00.types import ApprovalDisposition,SecurityStatus


def test_valid_approval(valid_bundle):
    r=ApprovalEvaluator(StructuralSignatureVerifier()).evaluate(valid_bundle.request,list(valid_bundle.approvals),{"required_roles":{"DOCTRINE_REVIEWER":1},"requester_cannot_approve":True},valid_bundle.request.requested_at); assert not r

def test_missing_role_fails(valid_bundle):
    r=ApprovalEvaluator(StructuralSignatureVerifier()).evaluate(valid_bundle.request,[],{"required_roles":{"DOCTRINE_REVIEWER":1}},valid_bundle.request.requested_at); assert any(x.code=="REQUIRED_APPROVAL_MISSING" for x in r)

def test_expired_approval_fails(valid_bundle):
    ap=replace(valid_bundle.approvals[0],expires_at=valid_bundle.request.requested_at-timedelta(seconds=1)); r=ApprovalEvaluator(StructuralSignatureVerifier()).evaluate(valid_bundle.request,[ap],{"required_roles":{"DOCTRINE_REVIEWER":1}},valid_bundle.request.requested_at); assert any(x.code=="APPROVAL_EXPIRED" for x in r)

def test_rejection_is_hard_failure(valid_bundle):
    ap=replace(valid_bundle.approvals[0],disposition=ApprovalDisposition.REJECT); r=ApprovalEvaluator(StructuralSignatureVerifier()).evaluate(valid_bundle.request,[ap],{"required_roles":{}},valid_bundle.request.requested_at); assert any(x.code=="EXPLICIT_REJECTION" for x in r)

def test_self_approval_fails(valid_bundle):
    ap=replace(valid_bundle.approvals[0],approver=valid_bundle.request.requested_by,role="CONTEXT_OWNER"); r=ApprovalEvaluator(StructuralSignatureVerifier()).evaluate(valid_bundle.request,[ap],{"required_roles":{"CONTEXT_OWNER":1},"requester_cannot_approve":True},valid_bundle.request.requested_at); assert any(x.code=="SELF_APPROVAL_FORBIDDEN" for x in r)

def test_valid_security_controls(valid_bundle):
    p={"required_controls":[x.control_id for x in valid_bundle.security_results],"known_controls":[x.control_id for x in valid_bundle.security_results]}; assert not SecurityHookEvaluator().evaluate(valid_bundle.request,list(valid_bundle.security_results),p,valid_bundle.request.requested_at)

def test_security_failure_is_hard_failure(valid_bundle):
    items=list(valid_bundle.security_results); items[0]=replace(items[0],status=SecurityStatus.FAIL); p={"required_controls":[x.control_id for x in items],"known_controls":[x.control_id for x in items]}; r=SecurityHookEvaluator().evaluate(valid_bundle.request,items,p,valid_bundle.request.requested_at); assert any(x.code=="SECURITY_CONTROL_NOT_PASS" for x in r)

def test_unknown_security_control_fails(valid_bundle):
    item=replace(valid_bundle.security_results[0],control_id="SEC_UNKNOWN"); p={"required_controls":[],"known_controls":[],"reject_unknown_controls":True}; r=SecurityHookEvaluator().evaluate(valid_bundle.request,[item],p,valid_bundle.request.requested_at); assert any(x.code=="UNKNOWN_SECURITY_CONTROL" for x in r)
