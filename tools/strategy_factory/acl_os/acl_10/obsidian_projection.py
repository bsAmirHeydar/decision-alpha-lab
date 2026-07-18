from __future__ import annotations
from pathlib import Path
from .canonical import digest_file, with_digest


def project(root: Path, run: dict, decision_bundle: dict, matrix: dict, runtime_manifest: dict) -> dict:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    summary = f"""---
title: ACL-10 Promotion State Summary
status: generated-reference
version: 1.0.0
tags: [acl-os, acl-10, generated]
---
# ACL-10 Promotion State Summary

- Promotion run: `{run['promotion_run_id']}`
- Source memory run: `{run['memory_run_id']}`
- Subjects evaluated: **{decision_bundle['decision_count']}**
- Promotion-review eligible: **{decision_bundle['promotion_review_eligible_count']}**
- Promotion executed: **0**
- Runtime candidates: **{runtime_manifest['runtime_candidate_count']}**
- Claim ceiling: `{run['claim_ceiling']}`

No report, memory admission or planner priority is interpreted as promotion authority.
"""
    (docs / "ACL10_PROMOTION_STATE_SUMMARY.md").write_text(summary, encoding="utf-8", newline="\n")
    states = ["# State Distribution", ""] + [
        f"- `{key}`: **{value}**" for key, value in decision_bundle["state_counts"].items()
    ]
    (docs / "PROMOTION_STATE_DISTRIBUTION.md").write_text(
        "\n".join(states) + "\n", encoding="utf-8", newline="\n"
    )
    unknown = sum(
        1
        for evaluation in matrix["evaluations"]
        for result in evaluation["results"]
        if result["status"] == "UNKNOWN"
    )
    (docs / "PROMOTION_PREREQUISITE_GAPS.md").write_text(
        f"# Promotion Prerequisite Gaps\n\nUnknown prerequisite results: **{unknown}**. "
        "UNKNOWN blocks promotion and is not treated as PASS.\n",
        encoding="utf-8",
        newline="\n",
    )
    files = [
        {"path": path.relative_to(root).as_posix(), "digest": digest_file(path)}
        for path in sorted(docs.glob("*.md"))
    ]
    return with_digest(
        {"schema_version": "1.0.0", "document_count": len(files), "documents": files},
        "projection_manifest_digest",
    )
