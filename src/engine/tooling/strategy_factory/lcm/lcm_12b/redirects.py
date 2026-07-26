from __future__ import annotations
from pathlib import PurePosixPath
from .canonical import stable_id

def redirect_stub(source_path: str, target_path: str, document_id: str, source_digest: str) -> str:
    title = PurePosixPath(source_path).stem.replace("_", " ")
    target_no_extension = target_path.rsplit(".", 1)[0] if target_path.lower().endswith(".md") else target_path
    return f'''---
title: "Redirect — {title}"
status: compatibility-redirect
phase_id: LCM-12B
claim_ceiling: LCM_12B_REFERENCE_ONLY
producer: src.engine.tooling.strategy_factory.lcm.lcm_12b.service:LCM12BDocumentationReconciliationService
source_document_id: {document_id}
source_digest: {source_digest}
canonical_target: {target_path}
generated_at: null
generated_time_semantics: DETERMINISTIC_FROM_BOUND_INPUTS_NO_WALL_CLOCK_IDENTITY
---
# Redirect

This legacy locator is retained for compatibility. The canonical document is [[{target_no_extension}|{title}]].

Do not edit this redirect as doctrine.
'''

def redirect_id(source_path: str, target_path: str) -> str:
    return stable_id("DOCREDIRECT", source_path, target_path)
