import pytest
from dataclasses import replace
from fp_i10_indicator import *
from fp_i10_indicator.errors import FPI10Error

def test_snapshot_allowed_exceeds_confirmed(engine):
 with pytest.raises(FPI10Error): replace(engine.snapshot,allowed_signal_count=999)
def test_buffer_wrong_count(engine):
 with pytest.raises(FPI10Error): replace(engine.snapshot.buffers,values=(1.0,))
def test_calculate_before_init():
 with pytest.raises(FPI10Error): IndicatorEngine().calculate(target_closed_m1=60000,upstream_state={})
def test_invalid_instance_chart(config):
 with pytest.raises(FPI10Error): build_instance_identity(config,0,'TERM')
