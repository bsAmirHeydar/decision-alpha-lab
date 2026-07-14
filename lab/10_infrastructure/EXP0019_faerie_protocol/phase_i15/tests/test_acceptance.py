from fp_i15_paper import *
def test_source_acceptance_pass():
 a=build_acceptance(True,True,True,True,True);assert a.source_status==AcceptanceStatus.PASS and a.paper_ready and not a.live_ready
def test_metaeditor_pending(): assert build_acceptance(True,True,True,True,True).metaeditor_status==AcceptanceStatus.PENDING
def test_failure_blocks_source(): assert build_acceptance(False,True,True,True,True).source_status==AcceptanceStatus.FAIL
