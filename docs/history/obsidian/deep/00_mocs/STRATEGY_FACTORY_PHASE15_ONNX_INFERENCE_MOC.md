# Strategy Factory Phase 15 — ONNX Export and MQL5 Inference MOC

## Core chain

[[docs/strategy_factory_implementation/phase15/05_PHASE14_RELEASE_CONSUMPTION|Governed release]] → [[docs/strategy_factory_implementation/phase15/08_ONNX_EXPORT_PLAN|Export plan]] → [[docs/strategy_factory_implementation/phase15/17_FEATURE_ORDER_CONTRACT|Feature order]] → [[docs/strategy_factory_implementation/phase15/19_PREPROCESSING_MANIFEST|Preprocessing]] → [[docs/strategy_factory_implementation/phase15/24_MODEL_MANIFEST|ONNX manifest]] → [[docs/strategy_factory_implementation/phase15/37_STARTUP_GUARD|Startup guard]] → [[docs/strategy_factory_implementation/phase15/49_CROSS_LANGUAGE_PARITY|Parity]] → [[docs/strategy_factory_implementation/phase15/65_PHASE16_HANDOFF|Phase 16 handoff]].

## Safety boundary

The terminal has prediction authority only. Trade selection, allocation, risk and execution remain absent. Read [[docs/strategy_factory_implementation/phase15/36_PREDICTION_ONLY_AUTHORITY|Prediction-only authority]] and [[docs/strategy_factory_implementation/phase15/39_FAIL_CLOSED_MATRIX|Fail-closed matrix]] before modifying the runtime.
