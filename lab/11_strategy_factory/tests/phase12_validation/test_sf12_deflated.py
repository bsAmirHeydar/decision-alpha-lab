from strategy_factory_validation import deflated_sharpe_probability

def test_more_trials_raise_expected_maximum():
 a=deflated_sharpe_probability("t",0.2,2,60);b=deflated_sharpe_probability("t",0.2,100,60);assert b.expected_max_sharpe>a.expected_max_sharpe;assert b.deflated_probability<a.deflated_probability

def test_probability_is_bounded():
 r=deflated_sharpe_probability("t",0.4,20,80,0.1,3.5);assert 0<=r.deflated_probability<=1
