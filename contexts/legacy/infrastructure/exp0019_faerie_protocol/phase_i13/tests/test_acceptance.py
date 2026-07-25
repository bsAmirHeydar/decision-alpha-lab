from fp_i13_release import *
def _manifest():return build_release_manifest({'a':'0'*64})
def test_pending_compile_yields_source_acceptance():
 gs=(gate('REPLAY',GateStatus.PASS,(),'0'*64),gate('METAEDITOR',GateStatus.PENDING,('PENDING',),'1'*64));r=build_acceptance(_manifest(),gs);assert r.status==AcceptanceStatus.SOURCE_ACCEPTED_EXTERNAL_COMPILE_PENDING and not r.production_release_ready
def test_all_pass_yields_accepted():
 gs=(gate('REPLAY',GateStatus.PASS,(),'0'*64),gate('METAEDITOR',GateStatus.PASS,(),'1'*64));assert build_acceptance(_manifest(),gs).status==AcceptanceStatus.ACCEPTED
def test_failed_gate_rejects():assert build_acceptance(_manifest(),(gate('X',GateStatus.FAIL,('FAIL',),'0'*64),)).status==AcceptanceStatus.REJECTED
