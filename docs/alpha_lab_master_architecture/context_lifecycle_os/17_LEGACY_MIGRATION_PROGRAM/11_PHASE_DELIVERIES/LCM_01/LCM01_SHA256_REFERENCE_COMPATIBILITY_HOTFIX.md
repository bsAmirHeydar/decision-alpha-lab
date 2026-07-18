---
title: "LCM-01 SHA-256 Reference Compatibility Hotfix"
status: implemented-reference
version: 1.0.0
updated: 2026-07-18
tags: [acl-os, lcm, lcm-01, integrity, sha256, windows]
phase_id: LCM-01
claim_ceiling: INSTALLATION_VERIFIER_COMPATIBILITY_ONLY
---
# LCM-01 SHA-256 Reference Compatibility Hotfix

## Incident

The first cross-platform verifier accepted CRLF/LF equivalence but rejected the algorithm-qualified digest representation used by the frozen LCM-00 baseline manifest:

```text
sha256:<64 lowercase hexadecimal characters>
```

The focused tests had exercised only the bare 64-character representation. Package verification and all phase tests passed, but installation verification stopped before byte comparison with `INVALID_SHA256_REFERENCE` semantics.

## Correction

The verifier now normalizes exactly two representations:

1. bare 64-character SHA-256 digest;
2. `sha256:` followed by a 64-character SHA-256 digest.

Normalization is case-insensitive for the algorithm label and hexadecimal characters, and returns a lowercase bare digest for comparison.

## Fail-closed boundary

The following remain rejected:

- empty digest;
- wrong digest length;
- non-hexadecimal payload;
- another algorithm label;
- nested or repeated `sha256:` labels;
- content changes hidden behind EOL conversion;
- binary EOL conversion;
- missing files;
- symlinks;
- repository path escapes.

## Regression evidence

The focused suite covers:

- CRLF text against LF baseline;
- raw binary equality;
- prefixed SHA-256 text reference;
- prefixed SHA-256 binary reference;
- genuine text mutation;
- binary mutation;
- path escape;
- malformed digest forms.

## Authority boundary

This hotfix creates no migration, refactor, cutover, runtime, order, signing-key, live-trading, or capital authority.
