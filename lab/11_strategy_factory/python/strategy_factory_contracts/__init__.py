"""Python research mirror for the MQL5-first Strategy Factory contracts.

MQL5 is the runtime authority. This package mirrors canonical schemas for
research, training, validation, artifact ingestion, and cross-language tests.
"""
from .enums import Direction, FeatureQuality, FeatureType, TimestampPrecision, Compatibility
from .schema import SchemaIdentity
from .time import MarketTimestamp
from .records import BarRecord, AnatomyEvent, FeatureValue, FeatureSnapshot, ArtifactIdentity
from .registry import ContractRegistry, default_registry

__all__ = [
    "Direction", "FeatureQuality", "FeatureType", "TimestampPrecision", "Compatibility",
    "SchemaIdentity", "MarketTimestamp", "BarRecord", "AnatomyEvent", "FeatureValue",
    "FeatureSnapshot", "ArtifactIdentity", "ContractRegistry", "default_registry",
]
