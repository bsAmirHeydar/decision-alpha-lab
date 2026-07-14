from fp_i12_operator import *
def test_default_includes_all(items,snapshot):assert len(apply_filters(items,FilterConfig(),snapshot.computed_hash).included)==4
def test_relation_filter(items,snapshot):
 c=FilterConfig(relations=('AL',));r=apply_filters(items,c,snapshot.computed_hash);assert [x.semantic_id for x in r.included]==['SIG-1']
def test_direction_filter(items,snapshot):
 c=FilterConfig(directions=('BEARISH',));assert [x.semantic_id for x in apply_filters(items,c,snapshot.computed_hash).included]==['SIG-2']
def test_historical_filter(items,snapshot):assert all(not x.is_historical for x in apply_filters(items,FilterConfig(include_historical=False),snapshot.computed_hash).included)
def test_focus(items,snapshot):assert [x.semantic_id for x in apply_filters(items,FilterConfig(focus_semantic_id='SIG-4'),snapshot.computed_hash).included]==['SIG-4']
def test_filter_does_not_mutate(items,snapshot):
 h=sha256(items);apply_filters(items,FilterConfig(relations=('WW',)),snapshot.computed_hash);assert sha256(items)==h
