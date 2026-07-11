from strategy_factory_validation import white_reality_check

def test_reality_check_is_reproducible():
 data={"a":[0.5]*20,"b":[0.1,-0.1]*10,"c":[-0.2]*20}
 a=white_reality_check(data,200,7);b=white_reality_check(data,200,7);assert a==b;assert a.winner_trial_id=="a";assert 0<=a.bootstrap_p_value<=1
