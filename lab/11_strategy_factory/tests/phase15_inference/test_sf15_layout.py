from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
def test_required_phase15_layout():
 required=["mql5/Include/AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh","mql5/Experts/StrategyFactory/SF15_InferenceHost.mq5","mql5/Experts/StrategyFactoryTests/SF15_OnnxRuntimeSmokeTest.mq5","lab/11_strategy_factory/examples/phase15/reference_linear_classifier.onnx","docs/strategy_factory_implementation/phase15/00_PHASE_15_MOC.md"]
 for rel in required:assert (ROOT/rel).exists(),rel
