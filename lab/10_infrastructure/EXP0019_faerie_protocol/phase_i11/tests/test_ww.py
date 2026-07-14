from fp_i11_visual import *

def test_ww_projected(snapshot,cfg): assert len(project_ww(snapshot,cfg))==1
def test_ww_immutable(snapshot,cfg): assert project_ww(snapshot,cfg)[0].immutable
def test_ww_direction_style(snapshot,cfg): assert project_ww(snapshot,cfg)[0].style.style_id=='WW_BEAR'
def test_hide_ww(snapshot,cfg):
 from dataclasses import replace
 assert project_ww(snapshot,replace(cfg,show_ww=False))==[]
