from strategy_factory.decision import IdentityCalibrator, PiecewiseLinearCalibrator, PlattCalibrator


def test_calibrators_are_bounded():
    assert IdentityCalibrator().transform(2) == 1
    assert 0 < PlattCalibrator(1,0).transform(0) < 1
    piece = PiecewiseLinearCalibrator((0,1),(0.1,0.9))
    assert abs(piece.transform(.5)-.5) < 1e-9
