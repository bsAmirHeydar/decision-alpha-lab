from pathlib import Path
from saed_v4_constitution.crosswalk import build_crosswalk,validate_no_mutation
from saed_v4_constitution.core_boundary import capture_snapshot,compare_snapshots

def test_crosswalk_covers_i18():
 c=build_crosswalk(); assert any(e['phase']=='I18' for e in c['entries'])

def test_crosswalk_is_read_only(): assert validate_no_mutation(build_crosswalk())

def test_snapshot_stable(tmp_path):
 p=tmp_path/'src/engine/packages/strategy_factory_x'; p.mkdir(parents=True); (p/'a.py').write_text('x')
 a=capture_snapshot(tmp_path); b=capture_snapshot(tmp_path); assert compare_snapshots(a,b)['status']=='allow'

def test_snapshot_detects_modify(tmp_path):
 p=tmp_path/'src/engine/packages/strategy_factory_x'; p.mkdir(parents=True); f=p/'a.py'; f.write_text('x'); a=capture_snapshot(tmp_path); f.write_text('y'); b=capture_snapshot(tmp_path); assert compare_snapshots(a,b)['status']=='reject'
