from __future__ import annotations
from typing import Any

def summary_md(validation:dict[str,Any],decisions:dict[str,Any])->str:
    counts=decisions['decision_counts']
    return f'''---
title: ACL-07 Validation Summary — {validation['validation_id']}
status: generated-reference
tags: [acl-os, acl-07, validation-run]
---
# ACL-07 Validation Summary

- Validation ID: `{validation['validation_id']}`
- Run ID: `{validation['run_id']}`
- Batch ID: `{validation['batch_id']}`
- Claim ceiling: `{validation['claim_ceiling']}`
- Candidate count: **{decisions['candidate_count']}**
- Evidence insufficient: **{counts.get('EVIDENCE_INSUFFICIENT',0)}**
- Validation failed: **{counts.get('VALIDATION_FAILED',0)}**
- Baseline reference only: **{counts.get('BASELINE_REFERENCE_ONLY',0)}**
- Diagnostic excluded: **{counts.get('DIAGNOSTIC_EXCLUDED',0)}**
- Eligible for reporting: **{counts.get('VALIDATION_ELIGIBLE_FOR_REPORTING',0)}**

## Authority boundary

This projection is non-promotional. It does not establish alpha, execution parity, live readiness or capital authorization.
'''
def candidate_index_md(decisions:dict[str,Any])->str:
    lines=["---","title: ACL-07 Candidate Decision Index","status: generated-reference","tags: [acl-os, acl-07, decisions]","---","# Candidate Decision Index",""]
    for d in decisions["decisions"]:
        lines.append(f"- `{d['setup_id']}` — **{d['decision_status']}** — passed {d['gate_summary']['passed']}/{d['gate_summary']['total']}")
    return "\n".join(lines)+"\n"
