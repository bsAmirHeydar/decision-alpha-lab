# Install and verify Phase 15

1. Extract the patch at the repository root.
2. Confirm `mql5/Files/StrategyFactory/Models/phase15/reference_linear_classifier.onnx` exists and is 269 bytes.
3. Run `tools/strategy_factory/run_phase15_tests.ps1`.
4. Compile all four SF15 EAs using `tools/strategy_factory/compile_sf15_inference.ps1` and the local `metaeditor64.exe` path.
5. Run `SF15_InferenceContractsSelfTest`.
6. Run `SF15_OnnxRuntimeSmokeTest` in the terminal and Strategy Tester. It must report `8/8` parity vectors.
7. Run `SF15_InferenceDiagnostic` to confirm file fingerprint, model load, shape binding and scalar output.
8. Use `SF15_InferenceHost` only after the startup guard reports ready.

Do not activate a release when the terminal build, model size, FNV fingerprint, feature schema, feature order, transform hash, preprocessing manifest hash, calibration hash, tensor contract or parity evidence differs from the exact release bundle. There is no permissive fallback.
