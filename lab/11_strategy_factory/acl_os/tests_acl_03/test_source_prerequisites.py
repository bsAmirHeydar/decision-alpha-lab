import copy
import pytest
from tools.strategy_factory.acl_os.acl_03.source_snapshot import build_source_snapshot
from tools.strategy_factory.acl_os.acl_03.prerequisites import validate_prerequisites
from tools.strategy_factory.acl_os.acl_03.service import COMPILER_VERSION

def test_snapshot_is_deterministic(context_root,package):
    a=build_source_snapshot(context_root,package,COMPILER_VERSION);b=build_source_snapshot(context_root,package,COMPILER_VERSION);assert a==b

def test_prerequisites_pass(package,snapshot,permit,approval,readiness): assert validate_prerequisites(package,snapshot,permit,approval,readiness)["passed"]

@pytest.mark.parametrize("field,value,code",[("decision","DENY","ACL03_AUTHORITY_DENIED"),("action","WRONG","ACL03_AUTHORITY_ACTION_MISMATCH"),("subject_artifact_id","other","ACL03_AUTHORITY_SUBJECT_MISMATCH"),("live_order_submission_allowed",True,"ACL03_ILLEGAL_CAPITAL_AUTHORITY"),("capital_activation_allowed",True,"ACL03_ILLEGAL_CAPITAL_AUTHORITY")])
def test_authority_mutations_fail(package,snapshot,permit,approval,readiness,field,value,code):
    x=copy.deepcopy(permit);x[field]=value;r=validate_prerequisites(package,snapshot,x,approval,readiness);assert not r["passed"];assert code in {f["code"] for f in r["findings"]}

@pytest.mark.parametrize("mutation,code",[("decision","ACL03_SEMANTIC_APPROVAL_DENIED"),("subject","ACL03_SEMANTIC_SUBJECT_MISMATCH"),("digest","ACL03_SOURCE_CHANGED_AFTER_APPROVAL"),("roles","ACL03_SEPARATION_OF_DUTIES_MISSING")])
def test_approval_mutations_fail(package,snapshot,permit,approval,readiness,mutation,code):
    x=copy.deepcopy(approval)
    if mutation=="decision":x["decision"]="REJECT"
    elif mutation=="subject":x["subject_artifact_id"]="other"
    elif mutation=="digest":x["source_snapshot_digest"]="sha256:"+"0"*64
    else:x["approver_roles"]=["semantic_owner"]
    r=validate_prerequisites(package,snapshot,permit,x,readiness);assert not r["passed"];assert code in {f["code"] for f in r["findings"]}
