
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.strategy_factory.acl_os.acl_03.service import ACL03ContextCompilerService
from .acl03_bindings import build_rthp_bindings, validate_rthp_acl03_bundle
from .canonical_source import canonical_context_mirror


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def compile_rthp_acl03(
    package_root: Path,
    compiled_root: Path,
    binding_root: Path,
    authority_permit_path: Path,
    semantic_approval_path: Path,
    acl02_readiness_path: Path,
) -> dict[str, Any]:
    readiness_doc = _load(acl02_readiness_path)
    readiness = readiness_doc.get("readiness", readiness_doc)
    with canonical_context_mirror(package_root) as canonical_root:
        result = ACL03ContextCompilerService().compile(
            canonical_root,
            compiled_root,
            _load(authority_permit_path),
            _load(semantic_approval_path),
            readiness,
        )
    binding_bundle = build_rthp_bindings(package_root, compiled_root, binding_root)
    validation = validate_rthp_acl03_bundle(package_root, compiled_root, binding_root)
    return {
        "passed": bool(result["passed"] and validation["passed"]),
        "compilation_receipt_digest": result["receipt"]["receipt_digest"],
        "onboarding_decision": result["onboarding"]["decision"],
        "highest_state": result["onboarding"]["highest_state"],
        "binding_bundle_digest": binding_bundle["bundle_digest"],
        "validation": validation,
    }
