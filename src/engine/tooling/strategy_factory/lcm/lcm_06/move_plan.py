from __future__ import annotations

import re

from .canonical import content_id, digest_object
from .errors import PolicyError
from .path_policy import validate

SHA256_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def build(source_path, target_path, source_sha256):
    validate(source_path)
    validate(target_path)
    if source_path.casefold() == target_path.casefold():
        raise PolicyError("move source and target must differ")
    if not isinstance(source_sha256, str) or not SHA256_RE.fullmatch(source_sha256):
        raise PolicyError("invalid source SHA-256")
    out = {
        "schema_version": "1.0.0",
        "move_plan_id": content_id("MOVEPLAN", [source_path, target_path, source_sha256]),
        "source_path": source_path,
        "target_path": target_path,
        "source_sha256": source_sha256,
        "operation": "GIT_MV_PREVIEW",
        "semantic_edit_allowed": False,
        "execute_allowed": False,
        "source_delete_allowed": False,
        "target_materialization_allowed": False,
        "reason_code": "MOVE_PLAN_REFERENCE_ONLY",
        "move_plan_digest": None,
    }
    out["move_plan_digest"] = digest_object(out, "move_plan_digest")
    return out
