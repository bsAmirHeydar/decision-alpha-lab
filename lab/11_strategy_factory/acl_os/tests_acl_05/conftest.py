from __future__ import annotations
import sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
if str(ROOT) not in sys.path:
    sys.path.insert(0,str(ROOT))
from tools.strategy_factory.acl_os.acl_05.io import load_json
from tools.strategy_factory.acl_os.acl_05.service import ACL05ImmutableBatchService

@pytest.fixture(scope="session")
def repo_root(): return ROOT
@pytest.fixture(scope="session")
def acl04_root(): return ROOT/"lab/11_strategy_factory/acl_os/fixtures/acl_04/reference_factory"
@pytest.fixture(scope="session")
def fixture_root(): return ROOT/"lab/11_strategy_factory/acl_os/fixtures/acl_05"
@pytest.fixture(scope="session")
def inputs(fixture_root):
    return {
      "authority_permit":load_json(fixture_root/"authority_permit.json"),
      "batch_request":load_json(fixture_root/"batch_request.json"),
      "dataset_documents":[load_json(fixture_root/"dataset_snapshot.json")],
      "label_documents":[load_json(fixture_root/"label_forward_direction.json"),load_json(fixture_root/"label_path_diagnostic.json")],
      "split_contract":load_json(fixture_root/"split_contract.json"),
      "environment_lock":load_json(fixture_root/"environment_lock.json"),
      "compute_budget":load_json(fixture_root/"compute_budget.json"),
    }
@pytest.fixture(scope="session")
def reference_result(tmp_path_factory,acl04_root,fixture_root,inputs):
    out=tmp_path_factory.mktemp("acl05-reference")/"batch"
    return ACL05ImmutableBatchService().build(acl04_root=acl04_root,output_root=out,fixture_root=fixture_root,**inputs)
@pytest.fixture
def build(tmp_path,acl04_root,fixture_root,inputs,reference_result):
    def _build(output_name="out",force=False,**overrides):
        if not overrides and not force:
            return reference_result
        args={**inputs,**overrides}
        return ACL05ImmutableBatchService().build(acl04_root=acl04_root,output_root=tmp_path/output_name,fixture_root=fixture_root,**args)
    return _build
