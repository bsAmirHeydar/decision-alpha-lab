from tools.repository_paths import find_repository_root
from pathlib import Path
import json,yaml,hashlib
from tools.strategy_factory.lcm.lcm_08b.verify import verify_package

REPO=find_repository_root(__file__)
CTX=REPO/'contexts/legacy/strategy_factory/authored/CTX_EXP0015_INTERMARKET_TIME_EXPERIMENT_3CD87586_V1'
PILOT=REPO/'registry/legacy_context_migration/pilot_migrations/PILOTMIG_344455420C8CA68E865FD54135E891D7'

def test_context_contracts_and_authority_boundaries():
    manifest=yaml.safe_load((CTX/'context_manifest.yaml').read_text())
    assert manifest['consumer_cutover'] is False
    assert manifest['runtime_authority'] is False
    assert manifest['live_order_authority'] is False
    assert manifest['capital_authority'] is False
    assert manifest['legacy_source_sha256']=='sha256:99e5e03a4bf30a2ab94949e2ddc6cdc1d067f0441d25dbe0dc8a138026a9bd2f'

def test_source_immutable():
    p=REPO/'contexts/legacy/lab_experiments/EXP0015_intermarket_time_divergence/experiment.py'
    assert 'sha256:'+hashlib.sha256(p.read_bytes()).hexdigest()=='sha256:99e5e03a4bf30a2ab94949e2ddc6cdc1d067f0441d25dbe0dc8a138026a9bd2f'

def test_pilot_package_verifies():
    out=verify_package(PILOT)
    assert out['passed']
