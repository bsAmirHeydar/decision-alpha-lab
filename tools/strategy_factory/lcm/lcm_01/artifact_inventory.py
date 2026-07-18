from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Iterable, Iterator

from .classification import (
    LANGUAGE_BY_EXT,
    family_candidate,
    generated_likelihood,
    media_family,
    semantic_role,
)


def iter_artifact_rows(records: Iterable[dict]) -> Iterator[dict]:
    """Yield one deterministic inventory row per LCM-00 baseline record.

    The iterator intentionally avoids retaining a second in-memory copy of the
    entire repository inventory. LCM-01 must remain usable on large legacy
    repositories without weakening exact-path coverage.
    """

    for ordinal, record in enumerate(records, 1):
        path = record["path"]
        extension = record.get("extension") or Path(path).suffix.lower()
        family, family_confidence = family_candidate(path)
        role, role_confidence = semantic_role(path, extension)
        generated, generated_reason = generated_likelihood(path, extension)
        parts = path.split("/")
        unknown_reasons: list[str] = []
        if role == "UNKNOWN_ROLE":
            unknown_reasons.append("SEMANTIC_ROLE_UNKNOWN")
        if generated == "MIXED_OR_UNKNOWN":
            unknown_reasons.append("AUTHORSHIP_GENERATION_UNKNOWN")
        if record.get("binary"):
            unknown_reasons.append("BINARY_CONTENT_NOT_SEMANTICALLY_SCANNED")

        yield {
            "ordinal": ordinal,
            "path": path,
            "casefold_path": path.casefold(),
            "top_level_namespace": parts[0],
            "parent_namespace": "/".join(parts[:-1]),
            "filename": parts[-1],
            "extension": extension or "<none>",
            "language": LANGUAGE_BY_EXT.get(extension, "UNKNOWN"),
            "media_family": media_family(extension, bool(record.get("binary"))),
            "size_bytes": record["size_bytes"],
            "sha256": record["sha256"],
            "binary": bool(record.get("binary")),
            "mode_octal": record.get("mode_octal", ""),
            "source_layer_id": record.get("source_layer_id", "UNKNOWN"),
            "source_member": record.get("source_member", ""),
            "family_candidate": family,
            "family_confidence_bps": family_confidence,
            "semantic_role_candidate": role,
            "semantic_confidence_bps": role_confidence,
            "generated_likelihood": generated,
            "generated_reason": generated_reason,
            "scan_status": (
                "METADATA_ONLY" if record.get("binary") else "TEXT_SCAN_ELIGIBLE"
            ),
            "unknown_reasons": unknown_reasons,
            "destructive_action_authority": False,
            "semantic_conclusion_claimed": False,
        }


def build_artifact_rows(repo_root: Path, records: tuple[dict, ...]) -> list[dict]:
    """Compatibility wrapper retained for focused tests and downstream tools."""

    del repo_root
    return list(iter_artifact_rows(records))
