"""Context-owned end-to-end activation for RTHP research training.

The package consumes local, immutable market-data artifacts and delegates model
training to the already-existing Strategy Factory trainer engine. It does not
modify shared engines, context semantics, treatment logic, execution, or capital
controls.
"""
from .config import ActivationConfig, load_activation_config
from .materializer import RTHPHistoricalMaterializer, MaterializationResult
from .pipeline import RTHPTrainActivationPipeline

__all__ = [
    "ActivationConfig",
    "load_activation_config",
    "RTHPHistoricalMaterializer",
    "MaterializationResult",
    "RTHPTrainActivationPipeline",
]
