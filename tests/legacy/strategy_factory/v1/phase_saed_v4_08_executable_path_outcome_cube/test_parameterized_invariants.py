import pytest
from .helpers import cube
@pytest.mark.parametrize('idx',range(12))
def test_rows_preserve_net_cost_identity(idx):
 r=cube().rows[idx];assert abs(r.net_r-(r.gross_r-r.cost.total_cost_r))<1e-9
@pytest.mark.parametrize('idx',range(12,24))
def test_rows_nonnegative_excursions(idx):
 r=cube().rows[idx];assert r.mfe_points>=0 and r.mae_points>=0 and 0<=r.remaining_fraction<=1
