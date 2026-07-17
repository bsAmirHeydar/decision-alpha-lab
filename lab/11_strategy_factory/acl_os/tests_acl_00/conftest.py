from __future__ import annotations
import json
from pathlib import Path
import pytest
from tools.strategy_factory.acl_os.common import REPO_ROOT
from tools.strategy_factory.acl_os.acl_00.io import load_bundle

FIX=REPO_ROOT/"lab"/"11_strategy_factory"/"acl_os"/"fixtures"/"acl_00"
@pytest.fixture
def valid_bundle(): return load_bundle(FIX/"valid_semantic_transition.json")
