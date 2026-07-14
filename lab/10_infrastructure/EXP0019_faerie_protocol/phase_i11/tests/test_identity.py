from fp_i11_visual import *

def test_object_id_stable(cfg): assert object_id(cfg.object_namespace,ObjectKind.SESSION_BOX,'W')==object_id(cfg.object_namespace,ObjectKind.SESSION_BOX,'W')
def test_kind_changes_id(cfg): assert object_id(cfg.object_namespace,ObjectKind.SESSION_BOX,'W')!=object_id(cfg.object_namespace,ObjectKind.WEEK_BOX,'W')
def test_style_not_in_object_id(cfg):
 a=Anchor(AnchorType.TIME_PRICE,1,1);s=make_spec(namespace=cfg.object_namespace,semantic_id='X',kind=ObjectKind.HUNT_MARKER,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=a,style=STYLES['HUNT'],semantic_hash=canonical_sha256('x'))
 s2=make_spec(namespace=cfg.object_namespace,semantic_id='X',kind=ObjectKind.HUNT_MARKER,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=a,style=STYLES['CANDIDATE'],semantic_hash=canonical_sha256('x'))
 assert s.object_id==s2.object_id and s.projection_hash!=s2.projection_hash
def test_semantic_change_changes_projection(cfg):
 a=Anchor(AnchorType.TIME_PRICE,1,1);x=canonical_sha256('x');y=canonical_sha256('y')
 s=make_spec(namespace=cfg.object_namespace,semantic_id='X',kind=ObjectKind.HUNT_MARKER,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=a,style=STYLES['HUNT'],semantic_hash=x)
 s2=make_spec(namespace=cfg.object_namespace,semantic_id='X',kind=ObjectKind.HUNT_MARKER,layer=Layer.HUNTS,state=VisualState.VISIBLE,anchor=a,style=STYLES['HUNT'],semantic_hash=y)
 assert s.projection_hash!=s2.projection_hash

def test_object_name_mt5_safe(cfg): assert len(object_id(cfg.object_namespace,ObjectKind.CONFIRMED_SIGNAL,'SIGNAL-'+'X'*80))<=63
