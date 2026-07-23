# Alpha Lab LCM-16A Windows EOL Portability Hotfix

## Purpose

This bounded hotfix removes a false-positive integrity failure caused by LF/CRLF worktree representation differences on Windows while preserving byte-strict verification for binary files and semantic changes.

## Observed failure

`LCM-16A` package QA stopped at:

```text
ValueError: unapproved baseline drift outside AIEOS: ACL_OS_06_ARTIFACT_INVENTORY.csv
```

The locked LF representation is 61,140 bytes with SHA-256:

```text
9d31fc29d99420a931ac6763e8447341d05921f55ce3ec5a295f932bdca27a9d
```

The Windows CRLF worktree representation is 61,483 bytes. The 343-byte difference equals the line-count expansion introduced by CRLF. No semantic field, row, token, or Unicode content changes.

## Resolution

The integrity layer now accepts only these representations of valid UTF-8 text:

1. exact raw bytes;
2. LF-only line endings;
3. CRLF-only line endings.

It does **not** normalise spaces, tabs, quoting, Unicode, JSON values, CSV values, Markdown content, ordering, or binary bytes. A one-character semantic mutation still fails.

The same bounded matcher is used by:

- LCM-16A baseline amendment verification;
- LCM-15A historical candidate verification;
- LCM-15B relocation and redirect verification;
- LCM-15C lock-set verification.

The 242 AIEOS amendments remain manifest-bound and scope-limited. No additional amendment path is introduced.

## Claim ceiling

```text
LCM_16A_EOL_PORTABILITY_HOTFIX_REFERENCE_ONLY
```

This hotfix creates no deletion, runtime, live-order, network, credential, or capital authority.
