import pytest
from strategy_factory_runtime import RuntimeConfig, RunMode

def test_valid_config():
    cfg = RuntimeConfig("exp0017", "1.0.0", "run_001", run_mode=RunMode.ANATOMY_AUDIT)
    cfg.validate()

def test_invalid_config_rejected():
    with pytest.raises(ValueError):
        RuntimeConfig("bad id", "1.0.0", "run").validate()

def test_small_bus_rejected():
    with pytest.raises(ValueError):
        RuntimeConfig("s", "1.0.0", "r", audit_bus_capacity=4).validate()
