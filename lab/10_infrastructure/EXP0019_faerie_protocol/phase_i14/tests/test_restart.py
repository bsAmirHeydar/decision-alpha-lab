from fp_i14_diagnostic import *
def test_restart_parity_all_products(runs):
    for r in runs.values():
        cp=create_checkpoint(r,9);rr,val=resume_from_checkpoint(r.manifest,r.fixture_id,r.events,cp);assert val.disposition==CheckpointDisposition.ACCEPTED and compare_runs(r,rr).status==DifferentialStatus.PASS
def test_bad_checkpoint_rebuilds(runs):
    from dataclasses import replace
    r=runs[ProductKind.INDICATOR];cp=replace(create_checkpoint(r,5),payload_hash='0'*64);rr,val=resume_from_checkpoint(r.manifest,r.fixture_id,r.events,cp);assert val.disposition==CheckpointDisposition.REJECT_HASH and compare_runs(r,rr).status==DifferentialStatus.PASS
