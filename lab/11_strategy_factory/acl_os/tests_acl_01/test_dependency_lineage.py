from dataclasses import replace
from datetime import datetime,timezone
from tools.strategy_factory.acl_os.acl_01.dependency import DependencyEdge
from tools.strategy_factory.acl_os.acl_01.lineage import LineageEdge

def register_two(registry,descriptor,permit_factory):
    p=permit_factory("REGISTER_ARTIFACT",subject=descriptor.identity.artifact_id); assert not registry.register_artifact(descriptor,p)
    d2=replace(descriptor,identity=replace(descriptor.identity,artifact_id=descriptor.identity.artifact_id.replace("@1.0.0","-copy@1.0.0"),name="ctx-test-copy",digest="sha256:"+"2"*64),canonical_path="lab/11_strategy_factory/contexts/ctx-test-copy/doctrine/context.md")
    registry.artifacts[d2.identity.artifact_id]=d2
    return descriptor,d2

def test_dependency_acyclic(registry,descriptor,permit_factory):
    a,b=register_two(registry,descriptor,permit_factory); registry.dependencies=[DependencyEdge(b.identity.artifact_id,a.identity.artifact_id,"contract")]
    assert not registry.dep_graph.validate(registry.artifacts,registry.dependencies)

def test_dependency_cycle(registry,descriptor,permit_factory):
    a,b=register_two(registry,descriptor,permit_factory); edges=[DependencyEdge(a.identity.artifact_id,b.identity.artifact_id,"contract"),DependencyEdge(b.identity.artifact_id,a.identity.artifact_id,"contract")]
    assert any(x.code=="DEPENDENCY_CYCLE" for x in registry.dep_graph.validate(registry.artifacts,edges))

def test_dependency_direction(registry,descriptor,permit_factory):
    a,b=register_two(registry,descriptor,permit_factory); a=replace(a,layer="contracts"); b=replace(b,layer="runtime"); registry.artifacts[a.identity.artifact_id]=a; registry.artifacts[b.identity.artifact_id]=b
    assert any(x.code=="DEPENDENCY_DIRECTION_VIOLATION" for x in registry.dep_graph.validate(registry.artifacts,[DependencyEdge(a.identity.artifact_id,b.identity.artifact_id,"runtime")]))

def test_lineage_requires_transformation(registry,descriptor,permit_factory):
    a,b=register_two(registry,descriptor,permit_factory); edge=LineageEdge("LIN_1",a.identity.artifact_id,b.identity.artifact_id,"derived_from",None,datetime.now(timezone.utc),{})
    assert any(x.code=="LINEAGE_TRANSFORMATION_MISSING" for x in registry.lineage_graph.validate(registry.artifacts,[edge]))

def test_lineage_cycle(registry,descriptor,permit_factory):
    a,b=register_two(registry,descriptor,permit_factory); now=datetime.now(timezone.utc)
    edges=[LineageEdge("L1",a.identity.artifact_id,b.identity.artifact_id,"derived_from","T1",now,{}),LineageEdge("L2",b.identity.artifact_id,a.identity.artifact_id,"derived_from","T2",now,{})]
    assert any(x.code=="LINEAGE_CYCLE" for x in registry.lineage_graph.validate(registry.artifacts,edges))
