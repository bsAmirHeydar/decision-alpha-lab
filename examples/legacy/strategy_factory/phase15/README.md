# Phase 15 deterministic reference bundle

This directory contains a complete exact-version export bundle for `sf15.reference.linear_classifier@1.0.0`. The ONNX file is a float32 scalar graph with a fixed `[1,4]` input, a fixed `[1,1]` output and only `MatMul` and `Add` operators. The terminal applies the separately governed preprocessing and sigmoid calibration contracts.

The authoritative offline SHA-256 is `3e0fa5825e5656cfefdcf34bb9e05e1844ab231c8dbb74150619068c392fcac8`. The terminal startup fingerprint is `1e623513209288b3` and the exact file size is `269` bytes. The parity corpus contains eight vectors including all-missing and partially-missing rows.
