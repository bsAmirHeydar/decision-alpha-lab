import pytest
from fp_i02_kernel.enums import QuotaConsumptionPolicy
from fp_i09_ledger.contracts import LedgerConfig
from fp_i09_ledger.errors import FPI09Error

def test_config_hash_stable(config): assert config.config_hash==config.config_hash and len(config.config_hash)==64
def test_live_forbidden():
    with pytest.raises(FPI09Error): LedgerConfig('C','P','E','0'*64,live_execution_enabled=True)
def test_consumption_policy_must_be_unset():
    with pytest.raises(FPI09Error): LedgerConfig('C','P','E','0'*64,quota_consumption_policy=QuotaConsumptionPolicy.FILLED)
def test_noncanonical_scope_rejected():
    with pytest.raises(FPI09Error): LedgerConfig('C','P','E','0'*64,quota_scope='PER_SYMBOL')
def test_noncanonical_winner_rejected():
    with pytest.raises(FPI09Error): LedgerConfig('C','P','E','0'*64,winner_policy='FIRST_CONFIRM')
