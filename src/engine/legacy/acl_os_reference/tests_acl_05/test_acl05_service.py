from pathlib import Path
from src.engine.tooling.strategy_factory.acl_os.acl_05.canonical import digest_object
from src.engine.tooling.strategy_factory.acl_os.acl_05.io import load_json
from src.engine.tooling.strategy_factory.acl_os.acl_05.replay import verify_frozen_batch

def test_reference_build_passes(build):
    r=build(); assert r["passed"] and r["research_candidate_count"]==11 and r["diagnostic_candidate_count"]==1

def test_batch_is_frozen(build):
    r=build(); assert r["batch"]["state"]=="FROZEN" and not r["batch"]["material_mutation_allowed"]

def test_same_material_same_batch_id(build):
    a=build("a"); b=build("b"); assert a["batch_id"]==b["batch_id"]

def test_same_material_same_semantic_manifest(build):
    a=build("a"); b=build("b"); assert a["batch_manifest"]["batch_manifest_digest"]==b["batch_manifest"]["batch_manifest_digest"]

def test_reference_replay_passes(build):
    r=build(); report=verify_frozen_batch(Path(r["output_root"])); assert report["passed"]

def test_output_contains_acl06_handoff(build):
    r=build(); h=load_json(Path(r["output_root"])/"handoff/acl06_handoff.json"); assert h["handoff_type"]=="ACL05_TO_ACL06"

def test_receipt_binds_output_manifest(build):
    r=build(); assert r["receipt"]["output_manifest_digest"]==r["output_manifest"]["manifest_digest"]

def test_no_execution_authority(build):
    r=build(); assert not r["handoff"]["live_order_submission_allowed"] and not r["handoff"]["capital_activation_allowed"]

def test_nonempty_output_denied(build,tmp_path):
    p=tmp_path/"out"; p.mkdir(); (p/"foreign.txt").write_text("x")
    import pytest
    with pytest.raises(Exception): build(force=True)

def test_generated_docs_exist(build):
    r=build(); root=Path(r["output_root"]); assert (root/"docs/ACL05_BATCH_SUMMARY.md").is_file() and (root/"docs/FROZEN_CANDIDATE_INDEX.md").is_file()
