import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[4]
PY_ROOT=ROOT/"lab/11_strategy_factory/python"
if str(PY_ROOT) not in sys.path: sys.path.insert(0,str(PY_ROOT))
EX=ROOT/"lab/11_strategy_factory/examples/saed_v4_30"
def load(name): return json.loads((EX/name).read_text(encoding="utf-8"))
@pytest.fixture
def inputs():
 return {"config":load("FULL_REFERENCE_CONFIG.JSON"),"upstream":load("UPSTREAM_V4_29_DOCUMENTS.JSON"),"protocol":load("REPLICATION_PROTOCOL.JSON"),"package":load("REPLICATION_PACKAGE_MANIFEST.JSON"),"labs":load("REPLICATION_LABS.JSON"),"environments":load("LAB_ENVIRONMENTS.JSON"),"payload":load("SYNTHETIC_REPLICATION_PAYLOAD.JSON")}
@pytest.fixture
def result(inputs):
 from saed_v4_independent_multi_lab_replication.service import run
 return run(inputs["config"],inputs["upstream"],inputs["protocol"],inputs["package"],inputs["labs"],inputs["environments"],inputs["payload"])
