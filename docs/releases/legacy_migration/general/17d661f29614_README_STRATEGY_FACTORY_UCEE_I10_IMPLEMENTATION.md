# Strategy Factory UCEE — UCE-I10 Deep Multi-View Pack

## Delivery

UCE-I10 v1.1.0 implements the deep representation and qualification layer that follows the accepted Context, classical baseline, and advanced task packs. It is deliberately contract-first and fail-closed: deep capacity is admitted only after support, known-time, future-perturbation, stable-dimension, and classical-baseline gates exist.

## Included surfaces

- **Sequence:** fixed causal windows, masks, time-major/feature-major layouts, deterministic temporal-convolution reference, GRU/Transformer adapter contracts.
- **Raster/Vision:** deterministic OHLCV rasterization, fixed channel/normalization contracts, pixel-level future-suffix audit, deterministic visual reference model, optional vision adapter boundary.
- **Graph:** versioned topology, canonical edge normalization, node known-time lineage, message-passing reference, topology/feature ablations.
- **Regime and novelty:** deterministic state clustering, transition evidence, standardized distance novelty, two-sided CUSUM, expert/global/abstain routing.
- **Fusion:** late weighted fusion, confidence-gated fusion, OOF-only stacked fusion, explicit missing-view policy, per-view ablation.
- **Transfer and compression:** source/target/final-test leakage boundary, deterministic distillation, symmetric int8 quantization.
- **Qualification:** non-bypassable admission, at least three unique seeds, failure accounting, stability, economics, calibration, ablation, export parity, latency, and fallback evidence.
- **Integration:** 17 algorithm descriptors, 10 native deterministic algorithms, five Trainer SDK plugins, 24 closed JSON schemas, MQL5 contract mirrors, diagnostics, conformance vectors, and detailed Obsidian documentation.

## Authority boundary

This phase is **research and qualification only**. It does not place, modify, or cancel orders; open positions; contact a broker; perform network calls; or claim that a model has market edge. Optional PyTorch, PyTorch Geometric, ONNX, HMM, or one-class implementations are adapter contracts until their dependencies and executable evidence are present.

## Validation entrypoint

### Linux/macOS

```bash
export PYTHONPATH="$PWD/lab/11_strategy_factory/python"
python -m pytest -q lab/11_strategy_factory/tests/phase_uce_i10_deep_views
python tools/strategy_factory/check_uce_i10_boundaries.py .
python tools/strategy_factory/check_uce_i10_mql5_static.py .
python tools/strategy_factory/generate_uce_i10_vectors.py . --verify-only
python tools/strategy_factory/validate_uce_i10_delivery.py .
```

### Windows PowerShell

```powershell
& .\tools\strategy_factory\run_uce_i10_tests.ps1 -RepoRoot $PWD
& .\tools\strategy_factory\compile_uce_i10_deep_views.ps1 -RepoRoot $PWD
```

The MetaEditor compile command must run on a Windows machine with MetaTrader 5 installed. Static MQL5 validation is not represented as a successful compile.

## Primary documentation

Start at:

`docs/strategy_factory_universal_context_exploitation_engine/implementation_program/phase_deliveries/uce_i10/00_UCE_I10_DELIVERY_MOC.md`

The delivery MOC links the architecture, contracts, failure policy, API reference, schema catalog, experiment examples, operator runbook, patch workflow, ADRs, and UCE-I11 handoff.
