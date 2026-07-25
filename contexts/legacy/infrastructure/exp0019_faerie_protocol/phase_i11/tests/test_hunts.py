from fp_i11_visual import *

def test_hunt_two_objects_each(snapshot,cfg,layout): assert len(project_hunts(snapshot,cfg,layout))==4
def test_hunt_marker_immutable(snapshot,cfg,layout): assert all(x.immutable for x in project_hunts(snapshot,cfg,layout))
def test_hunt_role_tooltip(snapshot,cfg,layout): assert any('HUNTER' in x.tooltip for x in project_hunts(snapshot,cfg,layout))
def test_hide_hunts(snapshot,cfg,layout):
 from dataclasses import replace
 assert project_hunts(snapshot,replace(cfg,show_hunts=False),layout)==[]
