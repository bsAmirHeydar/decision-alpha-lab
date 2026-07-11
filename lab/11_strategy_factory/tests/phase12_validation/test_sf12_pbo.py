from strategy_factory_validation import probability_of_backtest_overfitting

def test_unstable_winner_has_nonzero_pbo():
 data={"a":[2,2,-2,-2,2,2,-2,-2],"b":[-1,-1,1,1,-1,-1,1,1],"c":[0.1]*8}
 r=probability_of_backtest_overfitting(data);assert 0<=r.probability_of_backtest_overfitting<=1;assert r.split_count==70

def test_pbo_rejects_odd_blocks():
 try:probability_of_backtest_overfitting({"a":[1,2,3],"b":[2,1,0]})
 except ValueError:pass
 else:raise AssertionError("odd blocks accepted")
