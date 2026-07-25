from pathlib import Path
import copy
import pytest
from tools.strategy_factory.acl_os.acl_02.loader import ContextPackageLoader
from tools.strategy_factory.acl_os.acl_02.service import ACL02ContextIntakeService
from tools.strategy_factory.acl_os.acl_03.source_snapshot import build_source_snapshot
from tools.strategy_factory.acl_os.acl_03.service import COMPILER_VERSION
from tools.strategy_factory.acl_os.common import REPO_ROOT

@pytest.fixture
def context_root(): return REPO_ROOT/"src/engine/legacy/acl_os_reference/fixtures/acl_03/valid_context"
@pytest.fixture
def package(context_root):
    p=ContextPackageLoader(context_root).load();p.pop("_paths",None);return p
@pytest.fixture
def snapshot(context_root,package): return build_source_snapshot(context_root,package,COMPILER_VERSION)
@pytest.fixture
def permit(package): return {"permit_id":"PERMIT_ACL03_REF","decision":"ALLOW","action":"ACL03_COMPILE_CONTEXT","subject_artifact_id":package["manifest"]["artifact_id"],"live_order_submission_allowed":False,"capital_activation_allowed":False}
@pytest.fixture
def approval(package,snapshot): return {"decision":"APPROVE","subject_artifact_id":package["manifest"]["artifact_id"],"source_snapshot_digest":snapshot["snapshot_digest"],"approver_roles":["semantic_owner","independent_reviewer"],"approval_ids":["APR_SEM","APR_INDEPENDENT"]}
@pytest.fixture
def readiness(context_root,package):
    p={"decision":"ALLOW","action":"ACL02_EVALUATE_CONTEXT","subject_artifact_id":package["manifest"]["artifact_id"],"live_order_submission_allowed":False,"capital_activation_allowed":False}
    return ACL02ContextIntakeService().evaluate(context_root,p)["readiness"]
