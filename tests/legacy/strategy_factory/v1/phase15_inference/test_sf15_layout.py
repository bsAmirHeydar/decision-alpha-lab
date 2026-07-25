from tools.repository_paths import find_repository_root
from pathlib import Path
ROOT=find_repository_root(__file__)
def test_required_phase15_layout():
 required=["mql5/Include/AlphaLab/StrategyFactory/Inference/SF15_AllInference.mqh","mql5/Experts/StrategyFactory/SF15_InferenceHost.mq5","mql5/Tests/Experts/StrategyFactory/SF15_OnnxRuntimeSmokeTest.mq5","examples/legacy/strategy_factory/phase15/reference_linear_classifier.onnx","docs/strategy_factory_implementation/phase15/00_PHASE_15_MOC.md"]
 for rel in required:assert (ROOT/rel).exists(),rel
