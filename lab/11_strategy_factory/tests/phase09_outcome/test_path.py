import pytest
from strategy_factory_outcome import *
from strategy_factory_outcome.fixtures import bar
def test_mfe_mae_long():
    p=PathTracker(1,100,2,10);p.update(bar(1,2000,100,104,98.5,101));assert p.mfe_points==4;assert p.mae_points==1.5;assert p.mfe_r==2
def test_path_capacity():
    p=PathTracker(1,100,2,1);p.append(PathEventKind.REGISTERED,1000,100)
    with pytest.raises(OverflowError):p.append(PathEventKind.FILLED,2000,100)
