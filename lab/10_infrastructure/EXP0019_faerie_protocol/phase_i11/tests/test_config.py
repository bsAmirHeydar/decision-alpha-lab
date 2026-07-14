from fp_i11_visual import *

def test_config_hash_stable(cfg): assert cfg.config_hash==cfg.config_hash
def test_namespace_required():
 import pytest
 with pytest.raises(FPI11Error): ProjectionConfig('I','BAD::')
def test_history_bounds():
 import pytest
 with pytest.raises(FPI11Error): ProjectionConfig('I','FP19::I::',history_days=0)
def test_object_limit_bounds():
 import pytest
 with pytest.raises(FPI11Error): ProjectionConfig('I','FP19::I::',max_objects=99)
