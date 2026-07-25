from __future__ import annotations
from pathlib import Path
from .io import atomic_write

def onboarding_markdown(report:dict)->str:
    rows=[]
    for name,g in report["gates"].items():
        rows.append(f"| {name} | {'PASS' if g['passed'] else 'BLOCKED'} | {', '.join(g['reason_codes']) or '—'} |")
    obligations="\n".join(f"- `{x['code']}`" for x in report["open_obligations"])
    actions="\n".join(f"- `{x}`" for x in report["allowed_next_actions"])
    return f"""---
title: {report['context_id']} ACL-03 Onboarding Report
status: generated
context_id: {report['context_id']}
context_version: {report['context_version']}
report_digest: {report['report_digest']}
---
# ACL-03 Onboarding Report

> [!warning] Generated evidence
> This file is generated from machine-readable artifacts. Do not edit it manually. It does not prove alpha, external data quality, runtime parity, security hardening or capital authorization.

## Decision

- Decision: `{report['decision']}`
- Highest state: `{report['highest_state']}`
- Claim ceiling: `{report['claim_ceiling']}`

## Gate matrix

| Gate | Status | Reason codes |
|---|---|---|
{chr(10).join(rows)}

## Open obligations

{obligations}

## Allowed next actions

{actions}
"""
def write_projection(path:Path,report:dict)->None: atomic_write(path,onboarding_markdown(report).encode("utf-8"))
