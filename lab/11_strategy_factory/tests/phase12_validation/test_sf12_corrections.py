from strategy_factory_validation import bonferroni,holm,benjamini_hochberg

def test_holm_is_monotone_in_sorted_order():
 r=holm(("a","b","c"),(0.001,0.02,0.2));assert r.rejected==(True,True,False);assert r.adjusted_p_values[0]<=r.adjusted_p_values[1]

def test_bonferroni_and_bh_are_bounded():
 for r in (bonferroni(("a","b"),(0.01,0.8)),benjamini_hochberg(("a","b"),(0.01,0.8))):assert all(0<=x<=1 for x in r.adjusted_p_values)
