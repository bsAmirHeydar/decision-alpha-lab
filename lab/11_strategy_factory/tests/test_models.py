import numpy as np

from strategy_factory.models.baselines import LogisticRegressionGD, RidgeRegressor


def test_ridge_fits_linear_relation():
    x = np.arange(20, dtype=float).reshape(-1, 1)
    y = 2 * x[:, 0] + 3
    model = RidgeRegressor(alpha=0.001).fit(x, y)
    pred = model.predict(np.array([[21.0]]))[0]
    assert abs(pred - 45) < 1.0


def test_logistic_probability_is_bounded_and_ordered():
    x = np.array([[-2], [-1], [1], [2]], dtype=float)
    y = np.array([0, 0, 1, 1], dtype=float)
    model = LogisticRegressionGD(iterations=500, learning_rate=0.1).fit(x, y)
    p = model.predict_proba(x)[:, 1]
    assert np.all((p >= 0) & (p <= 1))
    assert p[-1] > p[0]
