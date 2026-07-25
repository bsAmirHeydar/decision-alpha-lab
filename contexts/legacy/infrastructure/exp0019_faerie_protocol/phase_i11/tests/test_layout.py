from fp_i11_visual import *

def test_price_per_pixel(layout): assert price_per_pixel(layout)==.02
def test_lane_step_tick_aligned(layout): assert lane_step(layout)%layout.tick_size==0
def test_lane_price_above(layout): assert lane_price(100,2,layout,True)>100
def test_lane_assignment_deterministic(snapshot): assert assign_lanes(snapshot.signals,6)==assign_lanes(tuple(reversed(snapshot.signals)),6)
def test_invalid_layout():
 import pytest
 with pytest.raises(FPI11Error): LayoutContext(1,1,100,.1,2)
