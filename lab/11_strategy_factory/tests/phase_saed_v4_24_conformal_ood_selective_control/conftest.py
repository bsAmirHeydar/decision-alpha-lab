from pathlib import Path
import json
import sys
import pytest
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'lab/11_strategy_factory/python'))
EX = ROOT / 'lab/11_strategy_factory/examples/saed_v4_24'
ART = ROOT / 'lab/11_strategy_factory/artifacts/saed_v4_24'
SCH = ROOT / 'lab/11_strategy_factory/schemas/saed_v4_24'
def load(path): return json.loads(Path(path).read_text(encoding='utf-8'))
@pytest.fixture(scope='session')
def config(): return load(EX / 'FULL_REFERENCE_CONFIG.JSON')
@pytest.fixture(scope='session')
def upstream(): return load(EX / 'UPSTREAM_V4_23_DOCUMENTS.JSON')
@pytest.fixture(scope='session')
def records(): return load(EX / 'CALIBRATION_SELECTION_DRIFT_RECORDS.JSON')
@pytest.fixture(scope='session')
def outputs(config, upstream, records):
    from saed_v4_conformal_ood_selective_control.service import run
    return run(config, upstream, records)
