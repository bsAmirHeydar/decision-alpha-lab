from __future__ import annotations

import json
from pathlib import Path

from tools.consolidation.uc04w1.characterize import (
    CANDIDATE_ID,
    EXPECTED_BODY_COMPACT,
    MEMBERS,
    PROPOSED_PRODUCTION_TARGET,
    characterize,
    extract_function,
    load_historical_candidate,
    sha256_file,
)

TRANSITION = Path("registry/consolidation/uc04/complete/w1_candidate_transition.json")


def _transition(repo_root: Path) -> dict | None:
    path = repo_root / TRANSITION
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None


def test_candidate_is_exact_historical_ten_member_cluster(repo_root: Path) -> None:
    transition = _transition(repo_root)
    if transition is None:
        inventory = characterize(repo_root)["candidate_inventory.json"]
        assert inventory["candidate_id"] == CANDIDATE_ID
        assert inventory["consumer_count"] == 10
        assert inventory["active_call_site_count"] == 41
        assert inventory["distinct_function_body_count"] == 1
        actual = {(row["artifact_path"], row["function_name"]) for row in inventory["members"]}
    else:
        assert transition["candidate_id"] == CANDIDATE_ID
        assert transition["member_count"] == 10
        assert transition["active_call_site_count"] == 41
        assert transition["status"] == "PASS"
        actual = {(row["artifact_path"], row["function_name"]) for row in transition["members"]}
    assert actual == {(path, function_name) for path, function_name, _ in MEMBERS}


def test_candidate_sources_are_historical_or_accepted_adapters(repo_root: Path) -> None:
    transition = _transition(repo_root)
    if transition is None:
        historical = load_historical_candidate(repo_root)
        historical_hashes = {row["artifact_path"]: row["artifact_sha256"] for row in historical["members"]}
        for relative, function_name, _ in MEMBERS:
            path = repo_root / relative
            assert sha256_file(path) == historical_hashes[relative]
            text = path.read_text(encoding="utf-8-sig")
            _, body, _, _ = extract_function(text, function_name)
            assert "".join(body.split()) == EXPECTED_BODY_COMPACT
    else:
        rows = {row["artifact_path"]: row for row in transition["members"]}
        for relative, function_name, _ in MEMBERS:
            path = repo_root / relative
            assert sha256_file(path) == rows[relative]["current_sha256"]
            text = path.read_text(encoding="utf-8-sig")
            assert rows[relative]["adapter_token"] in text
            assert function_name in text


def test_w1a_does_not_materialize_unapproved_original_target(repo_root: Path) -> None:
    assert not (repo_root / PROPOSED_PRODUCTION_TARGET).exists()
    decision = json.loads((repo_root / "registry/consolidation/uc04/w1/implementation_decision.json").read_text())
    assert decision["production_materialization_authorized"] is False
    assert decision["consumer_cutover_authorized"] is False
