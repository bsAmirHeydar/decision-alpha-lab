from fp_i11_visual import *

def test_winner_gets_badge(snapshot,cfg,layout): assert any(x.kind is ObjectKind.QUOTA_WINNER_BADGE for x in project_signals(snapshot,cfg,layout))
def test_suppressed_gets_overlay(snapshot,cfg,layout): assert any(x.kind is ObjectKind.SUPPRESSION_OVERLAY for x in project_signals(snapshot,cfg,layout))
def test_confirmed_immutable(snapshot,cfg,layout): assert all(x.immutable for x in project_signals(snapshot,cfg,layout))
def test_suppressed_hidden_standard(snapshot,cfg,layout):
 from dataclasses import replace
 c=replace(cfg,show_suppressed=False); assert not any(x.semantic_id.startswith('SIG-2') for x in project_signals(snapshot,c,layout))
def test_suppressed_visible_audit(snapshot,cfg,layout):
 from dataclasses import replace
 c=replace(cfg,show_suppressed=False,mode=VisualMode.AUDIT); assert any(x.semantic_id.startswith('SIG-2') for x in project_signals(snapshot,c,layout))
