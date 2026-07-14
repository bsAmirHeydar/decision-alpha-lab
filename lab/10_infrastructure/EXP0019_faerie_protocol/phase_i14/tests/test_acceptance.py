from fp_i14_diagnostic import *
def test_source_accepted_external_pending():
    gs=(gate('CROSS_PRODUCT',GateStatus.PASS,('OK',),sha256('1')),gate('METAEDITOR_COMPILE',GateStatus.PENDING,('PENDING',),sha256('2')),gate('LOCAL_TERMINAL_DIFFERENTIAL_RUNTIME',GateStatus.PENDING,('PENDING',),sha256('3')));a=build_acceptance(gs);assert a.source_accepted and not a.production_ready and a.status==GateStatus.PENDING
def test_hard_failure_fails():
    a=build_acceptance((gate('CROSS_PRODUCT',GateStatus.FAIL,('BAD',),sha256('x')),));assert not a.source_accepted and a.status==GateStatus.FAIL
