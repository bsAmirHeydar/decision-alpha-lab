from __future__ import annotations
import pytest
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records

def test_cluster_assignment_stable_and_occurrence_independent_where_declared():
    p=SyntheticBreakContextPackage(); o=p.observe(synthetic_records()[0])[0]; r=p.cluster_rules()[0]; c=ClusterCompiler()
    dims={"symbol":"EURUSD","timeframe_seconds":60,"signal_bar_open_ms":1710000000000,"direction":"long"}
    a=c.compile(r,o,dims); b=c.compile(r,o,dict(reversed(list(dims.items()))))
    assert a.cluster_id==b.cluster_id
    assert a.evidence_hash==b.evidence_hash

def test_missing_cluster_dimension_rejected():
    p=SyntheticBreakContextPackage(); o=p.observe(synthetic_records()[0])[0]
    with pytest.raises(ClusterError): ClusterCompiler().compile(p.cluster_rules()[0],o,{"symbol":"EURUSD"})

def test_all_required_cluster_kinds_are_representable():
    kinds={ClusterKind.OPPORTUNITY,ClusterKind.OVERLAPPING_PATH,ClusterKind.PARENT_CHILD,ClusterKind.SYMBOL_SESSION_DAY,ClusterKind.TREATMENT_SIBLING,ClusterKind.CUSTOM}
    for i,kind in enumerate(kinds):
        rule=ClusterRule(f"r{i}","1.0.0","owner",kind,("x",),{})
        assert rule.kind==kind and rule.rule_hash
