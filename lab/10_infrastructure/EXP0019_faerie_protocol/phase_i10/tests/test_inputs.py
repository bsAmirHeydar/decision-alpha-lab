import pytest
from fp_i10_indicator import *
from fp_i10_indicator.errors import FPI10Error

def test_pair_canonical(): assert canonical_pair_id('nq','ES')=='PAIR-ES-NQ'
def test_symbol_normalization(): assert normalize_symbol(' us500.cash ')=='US500.CASH'
def test_config_hash_deterministic(config): assert config.config_hash==config.config_hash
def test_primary_role_changes_hash():
 a=build_config(context_epoch='E',primary_symbol='ES',secondary_symbol='NQ'); b=build_config(context_epoch='E',primary_symbol='NQ',secondary_symbol='ES'); assert a.pair_id==b.pair_id and a.config_hash!=b.config_hash
@pytest.mark.parametrize('kwargs',[
 {'context_epoch':'E','primary_symbol':'ES','secondary_symbol':'ES'},
 {'context_epoch':'E','primary_symbol':'ES','secondary_symbol':'NQ','host_timeframe_minutes':7},
 {'context_epoch':'E','primary_symbol':'ES','secondary_symbol':'NQ','timer_seconds':0},
 {'context_epoch':'E','primary_symbol':'ES','secondary_symbol':'NQ','history_days':1},
])
def test_invalid_inputs(kwargs):
 with pytest.raises(FPI10Error): build_config(**kwargs)
