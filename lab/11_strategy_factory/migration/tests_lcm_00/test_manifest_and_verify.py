import json
from pathlib import Path
import pytest

from tools.strategy_factory.lcm.lcm_00.errors import IntegrityError
from tools.strategy_factory.lcm.lcm_00.manifest import build_baseline_manifest
from tools.strategy_factory.lcm.lcm_00.verify import verify_baseline_package, verify_repository_against_baseline


def test_reference_baseline_package_verifies(baseline_root):
    result=verify_baseline_package(baseline_root)
    assert result["passed"] is True
    assert result["record_count"] > 30000


def test_baseline_paths_are_sorted_and_unique(baseline_root):
    value=json.loads((baseline_root/"baseline_manifest.json").read_text(encoding="utf-8"))
    paths=[x["path"] for x in value["records"]]
    assert paths == sorted(paths)
    assert len(paths)==len(set(paths))


def test_repository_verifier_detects_changed_byte(tmp_path, baseline_root):
    package=tmp_path/"pkg"
    package.mkdir()
    # Minimal repository from first baseline record.
    manifest=json.loads((baseline_root/"baseline_manifest.json").read_text(encoding="utf-8"))
    first=next(x for x in manifest["records"] if x["kind"]=="FILE")
    source=(Path(__file__).resolve().parents[4]/first["path"])
    dst=package/first["path"]
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_bytes(source.read_bytes()+b"tamper")
    mini={**manifest,"record_count":1,"records":[first],"manifest_digest":""}
    from tools.strategy_factory.lcm.lcm_00.canonical import digest_object
    mini["manifest_digest"]=digest_object(mini,"manifest_digest")
    mini_root=tmp_path/"baseline"
    mini_root.mkdir()
    (mini_root/"baseline_manifest.json").write_text(json.dumps(mini),encoding="utf-8")
    result=verify_repository_against_baseline(package,mini_root,set())
    assert result["passed"] is False
    assert result["mismatch_count"] == 1


def test_undeclared_post_freeze_file_detected(tmp_path, baseline_root):
    empty={"schema_version":"1.0.0","baseline_id":"B","phase_id":"LCM-00","path_semantics":"ROOT_RELATIVE_POSIX_BYTE_EXACT","scope_policy_digest":"sha256:x","record_count":0,"records":[],"manifest_digest":""}
    from tools.strategy_factory.lcm.lcm_00.canonical import digest_object
    empty["manifest_digest"]=digest_object(empty,"manifest_digest")
    br=tmp_path/"b"; br.mkdir(); (br/"baseline_manifest.json").write_text(json.dumps(empty),encoding="utf-8")
    repo=tmp_path/"r"; repo.mkdir(); (repo/"unexpected.txt").write_text("x")
    result=verify_repository_against_baseline(repo,br,set())
    assert result["undeclared_addition_count"] == 1
