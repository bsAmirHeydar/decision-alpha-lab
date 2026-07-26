# LCM-16A package rehydration

The upstream audit package is verified with the LCM-16A verifier before the drill. A deterministic subset of manifest-owned artifacts is removed in a temporary copy, restored from the immutable source package and checked against every manifest SHA-256.

This proves bounded package rehydration. It does not claim MetaEditor, tester or external-consumer evidence that the upstream package explicitly marked UNKNOWN.
