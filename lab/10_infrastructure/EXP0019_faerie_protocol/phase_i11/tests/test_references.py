from fp_i11_visual import *

def test_reference_line_and_label(snapshot,cfg): assert len(project_references(snapshot,cfg))==4
def test_reference_price_anchor(snapshot,cfg): assert project_references(snapshot,cfg)[0].anchor.price1==105
def test_reference_symbol_in_tooltip(snapshot,cfg): assert 'ES' in project_references(snapshot,cfg)[0].tooltip
def test_consumed_stale(snapshot,cfg):
 from dataclasses import replace
 r=replace(snapshot.references[0],state=SemanticState.CONSUMED); s=replace(snapshot,references=(r,)); assert project_references(s,cfg)[0].state is VisualState.STALE
