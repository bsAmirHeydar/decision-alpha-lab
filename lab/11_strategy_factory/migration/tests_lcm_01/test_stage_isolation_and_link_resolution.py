import json

from tools.strategy_factory.lcm.lcm_01.docs_scan import _resolve
from tools.strategy_factory.lcm.lcm_01.stage_worker import STAGES


def test_parent_relative_document_link_stays_inside_repository():
    known = {
        "docs/domain/index.md",
        "docs/shared/target.md",
    }
    stem_map = {"target": ["docs/shared/target.md"]}
    status, resolved, _, _ = _resolve(
        "docs/domain/index.md",
        "docs/domain",
        "../shared/target.md",
        known,
        stem_map,
    )
    assert status == "RESOLVED_INTERNAL"
    assert resolved == "docs/shared/target.md"


def test_excessive_parent_traversal_is_reported_as_path_escape():
    known = {"docs/domain/index.md"}
    status, resolved, candidates, count = _resolve(
        "docs/domain/index.md",
        "docs/domain",
        "../../../../outside.md",
        known,
        {},
    )
    assert status == "PATH_ESCAPE"
    assert resolved == ""
    assert candidates
    assert count >= 1


def test_all_process_isolated_stage_receipts_are_published(survey_root):
    execution = json.loads(
        (survey_root / "operations/stage_execution_order.json").read_text(
            encoding="utf-8"
        )
    )
    assert execution["stage_order"] == list(STAGES)
    assert set(execution["stage_receipt_digests"]) == set(STAGES)
    for stage in STAGES:
        receipt = json.loads(
            (survey_root / "operations/stage_receipts" / f"{stage}.json").read_text(
                encoding="utf-8"
            )
        )
        assert receipt["stage_id"] == stage
        assert receipt["passed"] is True
        assert receipt["source_mutation_allowed"] is False
        assert receipt["source_move_performed"] is False
        assert receipt["source_delete_performed"] is False

    worker_results = json.loads(
        (survey_root / "operations/stage_worker_results.json").read_text(
            encoding="utf-8"
        )
    )
    for result in worker_results["stages"]:
        assert result["receipt"].startswith("operations/stage_receipts/")
        assert not result["receipt"].startswith("/")
        assert ".lcm01-staging-" not in result["receipt"]


def test_survey_stage_order_is_closed_and_deterministic(survey_root):
    execution = json.loads(
        (survey_root / "operations/stage_execution_order.json").read_text(
            encoding="utf-8"
        )
    )
    assert execution["stage_order"] == [
        "inventory",
        "mql5",
        "python",
        "documentation",
        "configuration",
        "structural",
    ]
    assert execution["source_mutation_allowed"] is False
