---
id: UCPS-B913F0A6C22D
title: "Root Relocation and Reference Rewrite Contract"
type: contract
status: canonical
domain: unified-consolidation-platform-seal
version: 1.0.0
created: 2026-07-25
updated: 2026-07-25
tags:
  - consolidation
  - uc03
  - relocation
---
# Root Relocation and Reference Rewrite Contract

## Relocation invariants

1. Every moved file has one source, one destination and one pre-move SHA-256 digest.
2. The destination bytes must equal the source bytes before reference rewriting begins.
3. Historical files under `releases/history/` remain byte-identical and are excluded from rewriting.
4. Active UTF-8 text references outside the historical archive are rewritten from the old basename to the canonical historical path.
5. A reference already using the canonical destination is never rewritten twice.
6. Binary files and undecodable text are not modified.
7. The operation is resume-safe when a source is absent and its hash-valid destination exists.
8. No semantic merge or executable relocation is implied by this contract.

## Destination taxonomy

```text
releases/history/<program>/<artifact-type>/<original-file-name>
```

Program and artifact-type assignments are deterministic and recorded in `ROOT_RELOCATION_MAP.jsonl`.

## Staging contract

`PATCH_FILE_INDEX.txt` is generated after application and contains the exact union of:

- static patch files;
- old root paths staged as deletions;
- relocated destination paths staged as additions;
- active reference files modified by rewriting;
- generated UC-03 Part 1 receipts.
