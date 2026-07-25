from __future__ import annotations

def summary_md(run:dict,index:dict,portfolio:dict,equiv:dict)->str:
    return f"""---
title: ACL-09 Memory and Active Planner Summary
status: generated-reference
version: 1.0.0
tags: [acl-os, acl-09, memory, planner]
---
# ACL-09 Memory and Active Planner Summary

- Memory run: `{run['memory_run_id']}`
- Source report: `{run['report_id']}`
- New memory entries: **{index['entry_count']}**
- Duplicate aliases: **{index['alias_count']}**
- Diagnostic quarantines: **{index['quarantine_count']}**
- Exact duplicates detected: **{equiv['exact_duplicate_count']}**
- Near-equivalence pairs: **{equiv['near_equivalence_count']}**
- Planner proposals: **{portfolio['proposal_count']}**
- Selected but unauthorized: **{portfolio['selected_count']}**

No alpha, promotion, research execution, order or capital authority is created.
"""

def memory_md(index:dict)->str:
    rows='\n'.join(f"- `{x['memory_entry_id']}` — {x['experience_class']}" for x in index['entries']) or '- None'
    return f"""---
title: ACL-09 Governed Memory Index
status: generated-reference
tags: [acl-os, acl-09, memory]
---
# Governed Memory Index

{rows}

History is append-only. Source semantics are not rewritten.
"""

def planner_md(portfolio:dict)->str:
    rows='\n'.join(f"- `{x['question_id']}` — **{x['proposal_status']}**" for x in portfolio['proposals']) or '- None'
    return f"""---
title: ACL-09 Bounded Research Planner
status: generated-reference
tags: [acl-os, acl-09, planner]
---
# Bounded Research Planner

{rows}

Proposals are not execution permission. A new permit and frozen batch remain mandatory.
"""

def duplicate_md(equiv:dict)->str:
    return f"""---
title: ACL-09 Duplicate and Equivalence Report
status: generated-reference
tags: [acl-os, acl-09, duplicates]
---
# Duplicate and Equivalence Report

- Source records: {equiv['record_count']}
- Unique fingerprints: {equiv['unique_fingerprint_count']}
- Exact duplicates: {equiv['exact_duplicate_count']}
- Near-equivalence pairs: {equiv['near_equivalence_count']}

Near equivalence never auto-merges source evidence.
"""
