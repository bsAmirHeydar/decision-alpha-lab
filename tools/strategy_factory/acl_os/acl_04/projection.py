from __future__ import annotations
from typing import Any


def candidate_markdown(candidate: dict[str, Any]) -> str:
    lines=[
        "---",f"title: {candidate['setup_id']}","status: generated-reference",f"context: {candidate['context_id']}",f"origin: {candidate['origin']}","tags: [acl-os, acl-04, generated-setup]","---","",
        f"# {candidate['setup_id']}","",
        "> [!warning] Generated projection",
        "> The machine-readable candidate JSON is authoritative. This note grants no trading or capital authority.","",
        "## Identity", "",
        f"- Candidate: `{candidate['candidate_id']}`",f"- Behavior digest: `{candidate['behavior_digest']}`",f"- Candidate digest: `{candidate['candidate_digest']}`",f"- Status: `{candidate['status']}`",f"- Treatment family: `{candidate['treatment_family']}`","",
        "## Policy clauses", "",
    ]
    for clause in candidate["policy_ir"]["clauses"]:
        lines.append(f"- `{clause['kind']}` / `{clause['action']}` / priority `{clause['priority']}` / `{clause['clause_id']}`")
    lines += ["","## Claim ceiling","","`SETUP_DEFINITION_REFERENCE_ONLY` — no alpha, parity, execution or capital claim.",""]
    return "\n".join(lines)


def factory_summary_markdown(result: dict[str, Any]) -> str:
    return f'''---
title: ACL-04 Dual Setup Factory — Generated Summary
status: generated-reference
tags: [acl-os, acl-04, generated-report]
---
# ACL-04 Dual Setup Factory — Generated Summary

> [!warning] Projection only
> Structured JSON artifacts are authoritative. This report does not establish edge, runtime parity, live readiness or capital authority.

## Bound Context

- Context: `{result["context_id"]}` @ `{result["context_version"]}`
- ACL-03 handoff: `{result["upstream_handoff_digest"]}`
- Factory receipt: `factory_receipt.json` (sealed after the output manifest)

## Counts

- Source candidates: **{result["source_candidate_count"]}**
- Canonical candidates: **{result["canonical_candidate_count"]}**
- Invalid candidates: **{result["invalid_candidate_count"]}**
- Diagnostic-only candidates: **{result["diagnostic_candidate_count"]}**

## Authority ceiling

`SETUP_DEFINITION_REFERENCE_ONLY`. Live order submission and capital activation remain forbidden.
'''
