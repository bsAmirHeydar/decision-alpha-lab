from __future__ import annotations

from .canonical import content_id, digest_object
from .errors import PolicyError
from .path_policy import validate
from .registries import REDIRECT_TYPES


def build(redirect_type, legacy_path, target_path):
    if redirect_type not in REDIRECT_TYPES:
        raise PolicyError("unknown redirect type")
    validate(legacy_path)
    validate(target_path)
    if legacy_path.casefold() == target_path.casefold():
        raise PolicyError("redirect source and target must differ")

    if redirect_type == "MQL_INCLUDE_WRAPPER":
        if not target_path.lower().endswith((".mqh", ".mq5")):
            raise PolicyError("MQL redirect target must be an MQL file")
        content = f"#pragma once\n#include <{target_path}>\n"
    elif redirect_type == "OBSIDIAN_REDIRECT_STUB":
        if not target_path.lower().endswith(".md"):
            raise PolicyError("Obsidian redirect target must be Markdown")
        note_target = target_path.removesuffix(".md")
        content = f"---\nstatus: deprecated-redirect\n---\n# Redirect\n\nCanonical: [[{note_target}]]\n"
    else:
        if not target_path.lower().endswith(".py"):
            raise PolicyError("Python redirect target must be a Python module")
        module = target_path.removesuffix(".py").replace("/", ".")
        content = f"from {module} import *  # compatibility shim\n"

    out = {
        "schema_version": "1.0.0",
        "redirect_id": content_id("REDIRECT", [redirect_type, legacy_path, target_path]),
        "redirect_type": redirect_type,
        "legacy_path": legacy_path,
        "target_path": target_path,
        "preview_content": content,
        "preview_only": True,
        "write_performed": False,
        "execution_authority": False,
        "reason_code": "REDIRECT_PREVIEW_REFERENCE_ONLY",
        "redirect_digest": None,
    }
    out["redirect_digest"] = digest_object(out, "redirect_digest")
    return out
