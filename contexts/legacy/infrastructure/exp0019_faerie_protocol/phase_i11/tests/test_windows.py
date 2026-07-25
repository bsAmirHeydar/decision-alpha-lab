from fp_i11_visual import *

def test_session_windows_project(snapshot,cfg): assert len(project_windows(snapshot,cfg))==2
def test_window_object_kind(snapshot,cfg): assert project_windows(snapshot,cfg)[0].kind is ObjectKind.SESSION_BOX
def test_complete_window_immutable(snapshot,cfg): assert project_windows(snapshot,cfg)[0].immutable
def test_hide_sessions(snapshot,cfg):
 from dataclasses import replace
 assert project_windows(snapshot,replace(cfg,show_sessions=False))==[]
