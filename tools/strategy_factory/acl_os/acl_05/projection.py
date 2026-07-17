from __future__ import annotations
from pathlib import Path

def write_summary(root: Path,batch: dict,candidates: dict,datasets: dict,labels: dict,split: dict,environment: dict,budget: dict,object_index: dict) -> None:
    text=f"""---
title: ACL-05 Frozen Research Batch {batch['batch_id']}
status: generated-immutable-projection
version: 1.0.0
tags: [acl-os, acl-05, research-batch]
---
# ACL-05 Frozen Research Batch

## Identity

- Batch: `{batch['batch_id']}`
- Context: `{batch['context_id']}@{batch['context_version']}`
- State: `{batch['state']}`
- Claim ceiling: `{batch['claim_ceiling']}`

## Frozen universe

- Research candidates: **{candidates['research_count']}**
- Diagnostic candidates: **{candidates['diagnostic_count']}**
- Dataset snapshots: **{len(datasets['snapshots'])}**
- Label contracts: **{len(labels['labels'])}**
- Split: `{split['split_id']}`
- Environment: `{environment['environment_id']}`
- Budget: `{budget['budget_id']}`
- CAS unique objects: **{object_index['object_count']}**
- CAS bytes: **{object_index['total_bytes']}**

## Authority

This projection is evidence for a frozen research definition only. It does not prove alpha, permit orders, activate capital, or establish MetaTrader/broker parity. The machine JSON artifacts are canonical; this note is generated and must not be hand-edited.
"""
    (root/"docs").mkdir(parents=True,exist_ok=True)
    (root/"docs/ACL05_BATCH_SUMMARY.md").write_text(text,encoding="utf-8",newline="\n")
    lines=["---","title: ACL-05 Frozen Candidate Index","status: generated-immutable-projection","---","# Frozen Candidate Index",""]
    for group,key in (("Research candidates","research_candidates"),("Diagnostic-only candidates","diagnostic_candidates")):
        lines += [f"## {group}",""]
        for ref in candidates[key]:
            lines.append(f"- `{ref['setup_id']}` — `{ref['status']}` — `{ref['behavior_digest']}`")
        lines.append("")
    (root/"docs/FROZEN_CANDIDATE_INDEX.md").write_text("\n".join(lines)+"\n",encoding="utf-8",newline="\n")
