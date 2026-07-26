from __future__ import annotations
from pathlib import Path
from .io import dump_json
from .canonical import with_digest

def project(root: Path, run: dict, decision: dict, assessment: dict, handoff: dict) -> dict:
    docs = root / 'docs'
    docs.mkdir(parents=True, exist_ok=True)
    summary = f"""---
title: ACL-11 Runtime Custody Summary
status: generated-reference
version: 1.0.0
tags: [acl-os, acl-11, runtime-custody]
---
# ACL-11 Runtime Custody Summary

- Run: `{run['runtime_custody_run_id']}`
- Promotion run: `{run['promotion_run_id']}`
- Runtime candidates: **{run['runtime_candidate_count']}**
- Custody decision: `{decision['decision']}`
- Custody state: `{decision['custody_state']}`
- Runtime generation allowed: **false**
- Runtime activation allowed: **false**
- Live order authority: **false**
- Capital authority: **false**

## Interpretation

The reference path contains no runtime-eligible candidate. ACL-11 therefore proves the fail-closed no-generation path and does not manufacture parity, signing or activation evidence.

## Next controlled phase

[[ACL_12_SECURITY_HARDENING]] receives a non-executable custody package.
"""
    (docs / 'ACL11_RUNTIME_CUSTODY_SUMMARY.md').write_text(summary, encoding='utf-8', newline='\n')
    lines = [
        '---',
        'title: ACL-11 Runtime Parity Evidence Gaps',
        'status: generated-reference',
        'version: 1.0.0',
        'tags: [acl-os, acl-11, parity]',
        '---',
        '# Runtime Parity Evidence Gaps',
        '',
    ]
    for result in assessment['results']:
        lines.append(f"- `{result['requirement_id']}` — **{result['status']}** — `{result['reason_code']}`")
    (docs / 'ACL11_RUNTIME_PARITY_GAPS.md').write_text('\n'.join(lines) + '\n', encoding='utf-8', newline='\n')
    manifest = with_digest(
        {
            'schema_version': '1.0.0',
            'documents': [
                'docs/ACL11_RUNTIME_CUSTODY_SUMMARY.md',
                'docs/ACL11_RUNTIME_PARITY_GAPS.md',
            ],
            'handoff_digest': handoff['handoff_digest'],
        },
        'projection_manifest_digest',
    )
    dump_json(root / 'docs/history/obsidian/base_projection_manifest.json', manifest)
    return manifest
