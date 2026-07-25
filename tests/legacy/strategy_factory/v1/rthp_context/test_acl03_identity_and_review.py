from tools.repository_paths import find_repository_root

import json
from pathlib import Path
import yaml

ROOT = find_repository_root(__file__)
PKG = ROOT / "contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"


def test_occurrence_identity_contains_acl03_aliases():
    occurrence = yaml.safe_load((PKG / "contracts/occurrence_contract.yaml").read_text(encoding="utf-8"))
    fields = set(occurrence["identity_fields"])
    assert {"context_id", "context_version", "anchor_time", "direction", "subject_key"} <= fields
    assert {"confirmation_close_time", "symbol_pair_id"} <= fields


def test_independent_review_is_closed_without_authority_escalation():
    review = json.loads((PKG / "governance/independent_context_review.json").read_text(encoding="utf-8"))
    assert review["decision"] == "APPROVE"
    assert review["reviewer_is_semantic_owner"] is False
    assert review["unresolved_domain_ambiguity_count"] == 0
    assert review["runtime_authority_created"] is False
    assert review["order_authority_created"] is False
    assert review["capital_authority_created"] is False
