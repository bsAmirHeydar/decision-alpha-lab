from tools.repository_paths import find_repository_root

import json
from pathlib import Path

from src.engine.tooling.strategy_factory.contexts.rthp.acl03_onboarding import compile_rthp_acl03

ROOT = find_repository_root(__file__)
PKG = ROOT / "contexts/legacy/strategy_factory/authored/CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1"
EVIDENCE = PKG / "generated/acl_03/evidence"


def test_acl03_recompile_is_digest_deterministic(tmp_path):
    a = compile_rthp_acl03(PKG, tmp_path / "a/compiled", tmp_path / "a/bindings", EVIDENCE / "authority_permit.json", EVIDENCE / "semantic_approval.json", EVIDENCE / "acl02_readiness.json")
    b = compile_rthp_acl03(PKG, tmp_path / "b/compiled", tmp_path / "b/bindings", EVIDENCE / "authority_permit.json", EVIDENCE / "semantic_approval.json", EVIDENCE / "acl02_readiness.json")
    assert a["passed"] and b["passed"]
    assert a["compilation_receipt_digest"] == b["compilation_receipt_digest"]
    assert a["binding_bundle_digest"] == b["binding_bundle_digest"]
