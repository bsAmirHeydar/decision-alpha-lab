# Typed MQL5 OnnxRun call and conversion policy

Phase 15 is the controlled boundary between offline model research and terminal-side prediction. It consumes only an exact governed release from Phase 14, produces a deterministic ONNX artifact and proves that MQL5 receives the same ordered features, performs the same preprocessing and emits numerically equivalent predictions. The phase deliberately stops before trade selection, capital allocation, risk sizing or order submission.

## Contract

The `33_ONNX_RUN_BOUNDARY` contract is versioned, hash-addressed and attributable to an exact model ID, model version, release hash, feature schema hash, feature-order hash, transform hash and calibration hash. Missing or contradictory lineage is a hard rejection, not a warning. Static shapes and float32 tensors are used so terminal behavior is bounded and reviewable.

## Runtime rule

MQL5 may load the ONNX file only during controlled startup. The startup guard validates terminal build, file size, runtime fingerprint, manifest identity, feature width and order, preprocessing lineage and calibration lineage before the session becomes ready. Each request is then checked for causal time ordering, exact width, finite observed values and matching lineage. No request can bypass preprocessing or the active manifest.

## Evidence

Acceptance requires deterministic export bytes, offline SHA-256, terminal FNV-1a fingerprint, structural inspection of graph operators, schema-valid manifests, the eight-vector golden corpus, raw-score parity, calibration parity, class parity, Python tests, MQL5 contract self-test, MetaEditor compilation and a local ONNX runtime smoke test. Evidence is append-only and points back to the Phase 14 release.

## Failure semantics

Any artifact mismatch, unsupported operator, incompatible build, shape mismatch, stale feature schema, transform drift, calibration drift, non-finite value, runtime error or parity breach leaves the model unavailable. There is no fallback to an ungoverned model and no silent tolerance widening. The prior exact release remains the only rollback target.

## Explicit boundary

The output is a typed prediction record. It does not decide whether to trade, rank candidates, size risk, reserve exposure, open a paper position or send a broker order. Those authorities begin only after Phase 16 and later safety gates.
