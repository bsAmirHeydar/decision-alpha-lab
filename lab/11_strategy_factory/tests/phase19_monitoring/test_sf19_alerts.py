from strategy_factory_monitoring import *

def test_alert_hysteresis_and_recovery():
    p=AlertPolicy("p","m",1,2,"HIGH",2,2,0,100);e=AlertEngine((p,))
    assert not e.observe("m",3,1,"c");f=e.observe("m",3,2,"c");assert f and f[0].state==AlertState.FIRING
    assert not e.observe("m",0,3,"c");r=e.observe("m",0,4,"c");assert r and r[0].state==AlertState.CLEAR

def test_alert_escalates_warning_to_critical():
    p=AlertPolicy("p","m",1,2,"HIGH",1,1,0,100);e=AlertEngine((p,));a=e.observe("m",1.5,1,"c");b=e.observe("m",3,2,"c");assert a[0].severity==Severity.WARNING;assert b[0].severity==Severity.CRITICAL

def test_unknown_metric_is_ignored():
    assert AlertEngine(reference_alert_policies()).observe("none",1,1,"c")==()
