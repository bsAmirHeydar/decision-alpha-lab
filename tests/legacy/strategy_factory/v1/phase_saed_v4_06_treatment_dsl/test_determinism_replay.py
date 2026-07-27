from dataclasses import replace
from .helpers import build,sources
from saed_v4_treatment_dsl.replay import build_replay_receipt
def test_source_order_is_nonsemantic():
 a=build();b=build(tuple(reversed(sources())));assert a.package_hash==b.package_hash;assert a.package_id==b.package_id
def test_replay_receipt_identical():
 a=build();b=build(tuple(reversed(sources())));r=build_replay_receipt(a,b);assert r.identical;assert not r.differing_paths
def test_semantic_change_changes_identity():
 src=list(sources());g=src[0];components=list(g.components);entry=components[2];params=dict(entry.parameters);params['buffer_points']='3.0';components[2]=replace(entry,parameters=tuple(sorted(params.items())));src[0]=replace(g,components=tuple(components));assert build(tuple(src)).package_hash!=build().package_hash
