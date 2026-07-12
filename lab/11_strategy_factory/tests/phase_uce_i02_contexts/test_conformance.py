from __future__ import annotations
from dataclasses import dataclass
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records, synthetic_future_mutations, exp0017_records

def test_reference_packages_pass_conformance():
    h=ContextConformanceHarness()
    a=h.run(SyntheticBreakContextPackage(),synthetic_records(),synthetic_future_mutations())
    b=h.run(EXP0017ContextPackage(),exp0017_records(),[])
    assert a.passed and b.passed
    assert a.replay_hash and b.replay_hash

def test_replay_hash_stable():
    h=ContextConformanceHarness(); p=SyntheticBreakContextPackage(); rows=synthetic_records()
    assert h.run(p,rows,[]).replay_hash==h.run(p,rows,[]).replay_hash

def test_future_mutation_is_ignored_by_reference_observer():
    p=SyntheticBreakContextPackage(); row=synthetic_records()[0]; changed=dict(row,future_close=999.0,future_high=1000.0)
    assert p.observe(row)[0].observation_hash==p.observe(changed)[0].observation_hash

def test_duplicate_input_replay_does_not_change_output_hash():
    p=SyntheticBreakContextPackage(); row=synthetic_records()[0]
    report=ContextConformanceHarness().run(p,[row,row],[])
    assert report.passed
