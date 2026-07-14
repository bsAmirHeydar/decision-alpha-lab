from fp_i11_visual import *

def test_first_diff_creates(snapshot,cfg,layout):
 m=ObjectManager(cfg.instance_id);specs=project_all(snapshot,cfg,layout);d=m.diff(specs,500);assert len(d.creates)==len(specs)
def test_second_diff_noop(snapshot,cfg,layout):
 m=ObjectManager(cfg.instance_id);specs=project_all(snapshot,cfg,layout);m.apply(m.diff(specs,500));d=m.diff(specs,500);assert len(d.unchanged)==len(specs)
def test_style_update_is_update(snapshot,cfg,layout):
 from dataclasses import replace
 m=ObjectManager(cfg.instance_id);specs=project_all(snapshot,cfg,layout);m.apply(m.diff(specs,500));x=specs[0];x2=replace(x,style=STYLES['INVALID'],projection_hash=canonical_sha256({'x':1}));d=m.diff((x2,)+specs[1:],500);assert len(d.updates)==1
def test_immutable_semantic_change_rejected(snapshot,cfg,layout):
 import pytest
 from dataclasses import replace
 m=ObjectManager(cfg.instance_id);specs=project_all(snapshot,cfg,layout);m.apply(m.diff(specs,500));idx=next(i for i,x in enumerate(specs) if x.immutable);x=specs[idx];x2=replace(x,semantic_hash=canonical_sha256('changed'),projection_hash=canonical_sha256('changed2'))
 ns=list(specs);ns[idx]=x2
 with pytest.raises(FPI11ImmutableViolation):m.diff(tuple(ns),500)
def test_mutable_delete(snapshot,cfg,layout):
 m=ObjectManager(cfg.instance_id);specs=project_all(snapshot,cfg,layout);m.apply(m.diff(specs,500));kept=tuple(x for x in specs if x.kind is not ObjectKind.HEALTH_BADGE);d=m.diff(kept,500);assert any('HEALTH' in x or x for x in d.deletes)
