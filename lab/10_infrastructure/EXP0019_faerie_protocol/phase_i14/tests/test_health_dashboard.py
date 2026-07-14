from fp_i14_diagnostic import *
def test_ready_health(): assert build_health((('EA','READY'),('IND','READY'),('PY','READY')),0).state==HealthState.READY
def test_degraded_health(): assert build_health((('EA','READY'),('IND','DEGRADED'),('PY','READY')),0).state==HealthState.DEGRADED
def test_blocked_health(): assert build_health((('EA','READY'),('IND','READY'),('PY','READY')),1).state==HealthState.BLOCKED
def test_dashboard_rows(runs):
    report=compare_products(tuple(runs.values()));h=build_health(tuple((p.value,'READY') for p in ProductKind),0);rows=dashboard_rows(report,h);assert ('overall_status','PASS') in rows
