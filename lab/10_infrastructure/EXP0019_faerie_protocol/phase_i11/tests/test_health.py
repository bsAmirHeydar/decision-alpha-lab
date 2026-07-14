from fp_i11_visual import *

def test_health_badge(snapshot,cfg): assert project_health(snapshot,cfg)[0].kind is ObjectKind.HEALTH_BADGE
def test_health_screen_anchor(snapshot,cfg): assert project_health(snapshot,cfg)[0].anchor.anchor_type is AnchorType.SCREEN_CORNER
def test_health_style_ready(snapshot,cfg): assert project_health(snapshot,cfg)[0].style.style_id=='HEALTH_READY'
