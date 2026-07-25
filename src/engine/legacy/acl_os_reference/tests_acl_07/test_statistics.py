from tools.strategy_factory.acl_os.acl_07.statistics import binomial_upper_tail,wilson_lower,benjamini_hochberg,max_drawdown,population_std

def test_binomial_none_on_zero(): assert binomial_upper_tail(0,0) is None
def test_binomial_perfect_small(): assert binomial_upper_tail(3,3)==0.125
def test_wilson_is_bounded(): assert 0<=wilson_lower(7,10)<=1
def test_wilson_none_on_zero(): assert wilson_lower(0,0) is None
def test_bh_monotone_mapping():
 q=benjamini_hochberg([('a',0.01),('b',0.02),('c',0.5)]); assert q['a']<=q['b']<=q['c']
def test_bh_preserves_none(): assert benjamini_hochberg([('a',None)])['a'] is None
def test_drawdown(): assert max_drawdown([1,-3,1])==-3
def test_population_std_zero(): assert population_std([2,2,2])==0
