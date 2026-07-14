from .contracts import *
from .enums import ProductKind

def validate_run(run):
    assert run.product==run.manifest.product
    assert run.inventory.event_count==len(run.events)
    assert tuple(e.sequence for e in run.events)==tuple(sorted(e.sequence for e in run.events))
    assert all(e.config_hash==run.manifest.config_hash for e in run.events)
    return True

def validate_cross_product(report):
    if report.status==DifferentialStatus.PASS: assert set(report.products)==set(ProductKind)
    return True
