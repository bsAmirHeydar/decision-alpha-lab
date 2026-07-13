import json,subprocess,sys,pytest
from strategy_factory_runtime_v3.registry import RuntimeAdapterRegistry
from strategy_factory_runtime_v3.migration import migrate_manifest
from strategy_factory_runtime_v3.errors import RuntimeContractError

def test_registry_capabilities_and_snapshot():
    r=RuntimeAdapterRegistry();r.register('native',object(),('float32','deterministic'));assert r.resolve('native',('float32',));assert r.snapshot()==(('native',('deterministic','float32')),)
def test_registry_rejects_duplicate():
    r=RuntimeAdapterRegistry();r.register('x',1)
    with pytest.raises(RuntimeContractError):r.register('x',2)
def test_registry_rejects_missing_capability():
    r=RuntimeAdapterRegistry();r.register('x',1,('a',))
    with pytest.raises(RuntimeContractError):r.resolve('x',('b',))
def test_manifest_migration_is_explicit():
    assert migrate_manifest({'version':'0.9.0'})['version']=='1.0.0';assert migrate_manifest({'version':'1.0.0'})=={'version':'1.0.0'}
def test_unknown_migration_rejected():
    with pytest.raises(RuntimeContractError):migrate_manifest({'version':'0.1.0'})
def test_cli_golden_parity():
    out=subprocess.check_output([sys.executable,'-m','strategy_factory_runtime_v3.cli','golden-parity'],text=True);payload=json.loads(out);assert payload['status']=='pass'
def test_cli_onnx_probe():
    out=subprocess.check_output([sys.executable,'-m','strategy_factory_runtime_v3.cli','probe-onnx'],text=True);payload=json.loads(out);assert 'available' in payload
