import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_02.loader import ContextPackageLoader
from src.engine.tooling.strategy_factory.acl_os.acl_02.security import classify_security
from src.engine.tooling.strategy_factory.acl_os.acl_02.authority_binding import validate_authority_binding

def pkg(root):p=ContextPackageLoader(root).load();p.pop("_paths");return p
def test_security_pass(valid_root):assert classify_security(pkg(valid_root))["passed"]
def test_underclassification_blocked(valid_root):assert not classify_security(pkg(valid_root.parent/"underclassified_context"))["passed"]
def test_permit_pass(valid_root,valid_permit):assert validate_authority_binding(pkg(valid_root)["manifest"],valid_permit)["passed"]
@pytest.mark.parametrize("field,value",[("decision","DENY"),("action","OTHER"),("subject_artifact_id","al://wrong"),("live_order_submission_allowed",True),("capital_activation_allowed",True)])
def test_permit_mutations_fail(valid_root,valid_permit,field,value):
 p=copy.deepcopy(valid_permit);p[field]=value;assert not validate_authority_binding(pkg(valid_root)["manifest"],p)["passed"]
def test_missing_permit_fails(valid_root):assert not validate_authority_binding(pkg(valid_root)["manifest"],None)["passed"]
