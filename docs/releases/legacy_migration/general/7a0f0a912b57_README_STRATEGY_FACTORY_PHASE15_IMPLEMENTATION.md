# Strategy Factory Phase 15 — ONNX Export and MQL5 Inference

Phase 15 implements the controlled boundary between governed offline models and terminal-side prediction. It adds deterministic pure-stdlib ONNX export for the Phase 13 linear/logistic baseline, exact Phase 14 release lineage, static float32 tensor contracts, immutable feature ordering, training-fitted preprocessing, calibration contracts, offline SHA-256 validation, terminal FNV-1a startup fingerprinting, native MQL5 `OnnxCreate`/`OnnxRun` integration, fail-closed startup and request guards, typed inference requests and results, parity evidence and runtime telemetry.

The reference graph has a fixed `[1,4]` input, a fixed `[1,1]` scalar output and only `MatMul` and `Add` operators. The terminal applies the separately governed preprocessing and sigmoid calibration contracts. The included model is 269 bytes, has SHA-256 `3e0fa5825e5656cfefdcf34bb9e05e1844ab231c8dbb74150619068c392fcac8`, and has terminal startup fingerprint `1e623513209288b3`.

Phase 15 grants **prediction authority only**. It contains no candidate selection, trade/skip decision, allocation, risk, paper-order or live-order authority.

## Local verification

```powershell
powershell -ExecutionPolicy Bypass -File .\tools\strategy_factory\run_phase15_tests.ps1

powershell -ExecutionPolicy Bypass `
  -File .\tools\strategy_factory\compile_sf15_inference.ps1 `
  -MetaEditor "C:\Program Files\MetaTrader 5\metaeditor64.exe"
```

After compilation, run `SF15_OnnxRuntimeSmokeTest` locally. Activation is valid only when all eight golden parity vectors pass within the declared float32 tolerances.
