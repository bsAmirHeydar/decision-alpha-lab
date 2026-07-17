import copy
import pytest
from tools.strategy_factory.acl_os.acl_05.authority import validate_authority
from tools.strategy_factory.acl_os.acl_05.candidate_freeze import freeze_candidates
from tools.strategy_factory.acl_os.acl_05.canonical import digest_object
from tools.strategy_factory.acl_os.acl_05.handoff_input import load_acl04_bundle

def redigest(doc,field): doc[field]=digest_object({k:v for k,v in doc.items() if k!=field}); return doc

def test_authority_valid(inputs,acl04_root):
    h=load_acl04_bundle(acl04_root)["handoff"]; assert validate_authority(inputs["authority_permit"],h)["passed"]

def test_authority_action_denied(inputs,acl04_root):
    h=load_acl04_bundle(acl04_root)["handoff"]; d=copy.deepcopy(inputs["authority_permit"]); d["action"]="ACL05_AUTHORIZE_ORDERS"; redigest(d,"permit_digest")
    with pytest.raises(Exception): validate_authority(d,h)

def test_authority_context_denied(inputs,acl04_root):
    h=load_acl04_bundle(acl04_root)["handoff"]; d=copy.deepcopy(inputs["authority_permit"]); d["context_id"]="CTX_OTHER"; redigest(d,"permit_digest")
    with pytest.raises(Exception): validate_authority(d,h)

def test_authority_order_denied(inputs,acl04_root):
    h=load_acl04_bundle(acl04_root)["handoff"]; d=copy.deepcopy(inputs["authority_permit"]); d["live_order_submission_allowed"]=True; redigest(d,"permit_digest")
    with pytest.raises(Exception): validate_authority(d,h)

def test_freeze_segregates_diagnostic(inputs,acl04_root):
    b=load_acl04_bundle(acl04_root); f=freeze_candidates(b["candidates"],inputs["batch_request"]); assert f["research_count"]==11 and f["diagnostic_count"]==1

def test_explicit_selection(inputs,acl04_root):
    b=load_acl04_bundle(acl04_root); d=copy.deepcopy(inputs["batch_request"]); eligible=next(c["setup_id"] for c in b["candidates"] if c["status"]=="ELIGIBLE_FOR_BATCH_DEFINITION"); d["candidate_selection"]={"mode":"EXPLICIT_SETUP_IDS","setup_ids":[eligible]}; redigest(d,"request_digest"); f=freeze_candidates(b["candidates"],d); assert f["research_count"]==1

def test_unknown_explicit_setup_denied(inputs,acl04_root):
    b=load_acl04_bundle(acl04_root); d=copy.deepcopy(inputs["batch_request"]); d["candidate_selection"]={"mode":"EXPLICIT_SETUP_IDS","setup_ids":["SETUP_NOT_REGISTERED"]}; redigest(d,"request_digest")
    with pytest.raises(Exception): freeze_candidates(b["candidates"],d)

def test_excluding_diagnostic_removes_it(inputs,acl04_root):
    b=load_acl04_bundle(acl04_root); d=copy.deepcopy(inputs["batch_request"]); d["diagnostic_policy"]="EXCLUDE"; redigest(d,"request_digest"); f=freeze_candidates(b["candidates"],d); assert f["diagnostic_count"]==0
