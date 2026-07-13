import pytest
from fp_i08_weekly.contracts import WWConfig
from fp_i08_weekly.errors import FPI08Error
from helpers import config

def test_config_hash_deterministic(): assert config().config_hash==config().config_hash
def test_config_hash_changes_with_store(): assert config().config_hash!=WWConfig('FP-CONTEXT-001','PAIR.A.B','3'*64,'2'*64).config_hash
@pytest.mark.parametrize('field,value',[('neutralization_policy','X'),('tradeability_policy','X'),('no_active_policy','X'),('resolution_policy','X')])
def test_noncanonical_policies_rejected(field,value):
    kw={'context_id':'FP-CONTEXT-001','pair_id':'PAIR.A.B','reference_store_hash':'1'*64,'confirmation_config_hash':'2'*64,field:value}
    with pytest.raises(FPI08Error):WWConfig(**kw)
