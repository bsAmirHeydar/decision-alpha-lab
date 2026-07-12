from __future__ import annotations
import pytest
from strategy_factory_contexts_v3 import *
from strategy_factory_contexts_v3.fixtures import synthetic_records

def frame():
    p=SyntheticBreakContextPackage(); o=p.observe(synthetic_records()[0])[0]; return p,o,p.build_feature_frame(o,{})

def descriptor(kind,view_id="x",feature_ids=("break.distance_atr",),shape=(1,),runtime=False):
    return RepresentationViewDescriptor(view_id,"1.0.0","alpha_lab",kind,feature_ids,shape,AvailabilityMode.RESEARCH,runtime,{})

def test_tabular_view_stable():
    p,o,f=frame(); r=RepresentationViewRegistry(); a=r.compile(p.view_descriptors()[0],f,{}); b=r.compile(p.view_descriptors()[0],f,{})
    assert a.view_hash==b.view_hash and a.view_instance_id==b.view_instance_id
    assert a.payload["columns"]==list(p.view_descriptors()[0].feature_ids)

def test_sequence_graph_intermarket_and_raster():
    p,o,f=frame(); r=RepresentationViewRegistry()
    seq=r.compile(descriptor(RepresentationKind.SEQUENCE,"seq",("break.distance_atr",),(1,3)),f,{"sequence_windows":{"break.distance_atr":[1.0,2.0,3.0]}}); assert len(seq.payload["values"][0])==3
    graph=r.compile(descriptor(RepresentationKind.GRAPH,"graph"),f,{"graph":{"nodes":["A","B"],"edges":[[0,1]],"node_features":{"A":[1.0]}}}); assert graph.payload["nodes"]==["A","B"]
    inter=r.compile(descriptor(RepresentationKind.INTERMARKET,"inter"),f,{"intermarket_symbols":["A","B"],"intermarket_matrix":[[1.0],[2.0]]}); assert inter.payload["symbols"]==["A","B"]
    raster=r.compile(descriptor(RepresentationKind.RASTER,"raster"),f,{"raster":[0.1,0.2],"raster_layout":"channels_first"}); assert raster.payload["layout"]=="channels_first"

def test_sparse_path_execution_portfolio_fused():
    p,o,f=frame(); r=RepresentationViewRegistry()
    assert r.compile(descriptor(RepresentationKind.SPARSE_EVENT,"sparse"),f,{"sparse_events":[{"t":1}]}).payload["events"]
    assert r.compile(descriptor(RepresentationKind.PATH_SIGNATURE,"path"),f,{"path_signature":[1.0,2.0],"signature_order":2}).payload["order"]==2
    assert r.compile(descriptor(RepresentationKind.EXECUTION,"exec"),f,{"execution_state":{"spread":2}}).payload["execution_state"]["spread"]==2
    assert r.compile(descriptor(RepresentationKind.PORTFOLIO,"port"),f,{"portfolio_state":{"gross":1}}).payload["portfolio_state"]["gross"]==1
    assert list(r.compile(descriptor(RepresentationKind.FUSED,"fused"),f,{"fused_parts":{"b":2,"a":1}}).payload["parts"])==["a","b"]

def test_missing_view_inputs_fail_closed():
    p,o,f=frame(); r=RepresentationViewRegistry()
    with pytest.raises(ViewError): r.compile(descriptor(RepresentationKind.SEQUENCE,"seq"),f,{})
    with pytest.raises(ViewError): r.compile(descriptor(RepresentationKind.GRAPH,"graph"),f,{})
    with pytest.raises(ViewError): r.compile(descriptor(RepresentationKind.TABULAR,"bad",("unknown",)),f,{})
