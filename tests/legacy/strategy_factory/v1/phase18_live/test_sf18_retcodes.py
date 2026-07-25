from strategy_factory_live import *

def test_retcode_classes_are_conservative():
    assert classify_retcode(0)==RetcodeClass.SUCCESS
    assert classify_retcode(10009)==RetcodeClass.SUCCESS
    assert classify_retcode(10024)==RetcodeClass.TRANSIENT
    assert classify_retcode(10019)==RetcodeClass.ACCOUNT_STATE
    assert classify_retcode(10030)==RetcodeClass.REQUEST_INVALID
    assert classify_retcode(99999)==RetcodeClass.UNKNOWN
    assert retcode_is_success(10008) and not retcode_is_success(10006)
