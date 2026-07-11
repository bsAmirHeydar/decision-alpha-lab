from strategy_factory_training import *

def test_binary_and_regression_labels():
    b=LabelContract("b","1",LabelKind.BINARY_NET_R,positive_threshold_r=0.1).with_hash()
    assert derive_label(0.11,False,True,True,b).value==1.0
    assert derive_label(0.10,False,True,True,b).value==0.0
    r=LabelContract("r","1",LabelKind.REGRESSION_NET_R,regression_floor_r=-1,regression_cap_r=1).with_hash()
    assert derive_label(4,False,True,True,r).value==1

def test_ambiguous_exclusion_is_explicit():
    c=LabelContract("b","1",LabelKind.BINARY_NET_R,ambiguous_policy=AmbiguousLabelPolicy.EXCLUDE).with_hash()
    d=derive_label(2,True,True,True,c);assert not d.available and d.reason=="ambiguous_excluded"
