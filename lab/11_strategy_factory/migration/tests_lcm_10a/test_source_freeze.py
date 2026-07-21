from .conftest import j,jl
def test_source_freeze_is_closed_and_non_destructive():
 s=j('source/source_freeze_summary.json');rows=jl('source/source_file_freeze.jsonl');assert s['source_file_count']==len(rows)==7382;assert all(not r['source_move_performed'] and not r['source_delete_performed'] and not r['semantic_refactor_performed'] for r in rows)
