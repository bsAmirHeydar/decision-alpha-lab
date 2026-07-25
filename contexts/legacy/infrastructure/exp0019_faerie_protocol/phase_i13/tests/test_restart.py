from fp_i13_release import *
def test_restart_parity_midpoint(fixture,instance): assert run_restart(fixture,instance,50).parity.status==ParityStatus.PASS
def test_restart_parity_near_start(fixture,instance): assert run_restart(fixture,instance,1).parity.status==ParityStatus.PASS
def test_restart_parity_near_end(fixture,instance): assert run_restart(fixture,instance,len(fixture.events)-1).parity.status==ParityStatus.PASS
def test_restart_checkpoint_restored(fixture,instance): assert run_restart(fixture,instance,40).checkpoint_disposition==CheckpointDisposition.RESTORED
