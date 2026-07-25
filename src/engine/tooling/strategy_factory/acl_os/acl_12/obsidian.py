from __future__ import annotations
from pathlib import Path
from .io import dump_json
from .canonical import with_digest
def project(root:Path,run:dict,decision:dict,matrix:dict,risk:dict,handoff:dict)->dict:
    docs=root/"docs"; docs.mkdir(parents=True,exist_ok=True)
    summary=f"""---
title: ACL-12 Security Hardening Summary
status: generated-reference
version: 1.0.0
tags: [acl-os, acl-12, security]
---
# ACL-12 Security Hardening Summary

- Run: `{run['security_hardening_run_id']}`
- Upstream runtime-custody run: `{run['runtime_custody_run_id']}`
- Security decision: `{decision['decision']}`
- Reference hardening passed: **{str(decision['reference_hardening_passed']).lower()}**
- Production security ready: **false**
- Runtime candidates: **0**
- Runtime activation: **false**
- Live order authority: **false**
- Capital authority: **false**

## Interpretation

ACL-12 verifies and hardens the reference security boundary. It does not claim production security because external attestations, privileged-workstation evidence, tested recovery, production monitoring, red-team evidence, CI branch-protection evidence and production key custody are unavailable.

## Next controlled phase

[[ACL_13_ONE_HOUR_ASSESSMENT_PRODUCT]] receives a non-capital security-readiness package.
"""
    (docs/"ACL12_SECURITY_HARDENING_SUMMARY.md").write_text(summary,encoding="utf-8",newline="\n")
    lines=["---","title: ACL-12 Security Control Matrix","status: generated-reference","version: 1.0.0","tags: [acl-os, acl-12, security-controls]","---","# Security Control Matrix",""]
    for r in matrix["results"]: lines.append(f"- `{r['control_id']}` — **{r['status']}** — `{r['reason_code']}`")
    (docs/"ACL12_SECURITY_CONTROL_MATRIX.md").write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")
    risks=["---","title: ACL-12 Open Production Security Risks","status: generated-reference","version: 1.0.0","tags: [acl-os, acl-12, risk]","---","# Open Production Security Risks",""]
    for r in risk["risks"]:
        if r["residual_state"]=="OPEN": risks.append(f"- `{r['threat_id']}` — **{r['inherent_severity']}** — `{r['next_action']}`")
    (docs/"ACL12_OPEN_PRODUCTION_SECURITY_RISKS.md").write_text("\n".join(risks)+"\n",encoding="utf-8",newline="\n")
    m=with_digest({"schema_version":"1.0.0","documents":["docs/ACL12_SECURITY_HARDENING_SUMMARY.md","docs/ACL12_SECURITY_CONTROL_MATRIX.md","docs/ACL12_OPEN_PRODUCTION_SECURITY_RISKS.md"],"handoff_digest":handoff["handoff_digest"]},"projection_manifest_digest"); dump_json(docs/"obsidian_projection_manifest.json",m); return m
