from fp_i05_reference.golden import golden_completed_n_window
from fp_i05_reference.store import build_store_snapshot,get_window,get_references_for_window
from fp_i05_reference.checkpoint import make_checkpoint,validate_checkpoint
from fp_i05_reference.enums import StoreHealth,CacheDisposition
from fp_i02_kernel.enums import WindowKind

def _snapshot():
 cfg,result,desc,agg,refs=golden_completed_n_window()
 return build_store_snapshot(cfg,'DATASET',result.revision.revision_id,(agg,),refs.references,desc.end_utc_ms),cfg,result,desc,agg,refs

def test_store_indexes_window_by_date_and_kind():
 s,cfg,result,desc,agg,refs=_snapshot()
 assert get_window(s,desc.trading_date,WindowKind.N).pair_window_id==agg.pair_window_id

def test_store_indexes_references_by_source_window():
 s,cfg,result,desc,agg,refs=_snapshot()
 assert len(get_references_for_window(s,agg.pair_window_id))==4

def test_store_snapshot_is_deterministic():
 a,*_= _snapshot();b,*_=_snapshot();assert a.semantic_hash==b.semantic_hash and a.index_hash==b.index_hash

def test_checkpoint_accepts_exact_payload_and_versions():
 s,cfg,result,desc,agg,refs=_snapshot();cp,payload=make_checkpoint(s,desc.end_utc_ms)
 assert validate_checkpoint(cp,payload,cfg.config_hash,result.revision.revision_id)[0] is CacheDisposition.ACCEPTED

def test_checkpoint_rejects_corrupt_payload():
 s,cfg,result,desc,agg,refs=_snapshot();cp,payload=make_checkpoint(s,desc.end_utc_ms)
 assert validate_checkpoint(cp,payload+'x',cfg.config_hash,result.revision.revision_id)[0] is CacheDisposition.REJECTED

def test_checkpoint_requires_exact_revision():
 s,cfg,result,desc,agg,refs=_snapshot();cp,payload=make_checkpoint(s,desc.end_utc_ms)
 assert validate_checkpoint(cp,payload,cfg.config_hash,'OTHER')[0] is CacheDisposition.REBUILD_REQUIRED

def test_evolving_reference_state_changes_store_not_window_identity():
 from fp_i05_reference.store import evolve_snapshot
 from fp_i05_reference.reference_engine import transition_reference
 from fp_i05_reference.enums import ReferenceTransition,TouchActor
 s,cfg,result,desc,agg,refs=_snapshot();updated,_=transition_reference(s.references[0],ReferenceTransition.HUNTER_TOUCH_OBSERVED,desc.end_utc_ms+60000,'E',TouchActor.HUNTER)
 evolved=evolve_snapshot(s,updated,desc.end_utc_ms+60000)
 assert evolved.semantic_hash!=s.semantic_hash
 assert [w.pair_window_id for w in evolved.pair_windows]==[w.pair_window_id for w in s.pair_windows]
