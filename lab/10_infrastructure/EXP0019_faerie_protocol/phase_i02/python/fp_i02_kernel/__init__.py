"""FP-I02 — Faerie Protocol core context types, identity, and reason-code kernel."""
from .canonical import canonical_json, canonical_sha256, projection_hash, semantic_hash, stable_id
from .config import (
    ConfigurationBundle,
    OperationalConfiguration,
    ProjectionConfiguration,
    SemanticConfiguration,
    canonical_research_bundle,
)
from .contracts import *
from .enums import *
from .errors import FPI02Error
from .identity import *
from .lifecycle import *
from .reason_codes import DEFAULT_REASON_REGISTRY, ReasonDescriptor, ReasonRegistry
from .registry import DEFAULT_CONTRACT_REGISTRY, ContractDescriptor, ContractRegistry
from .relations import DEFAULT_RELATION_REGISTRY, RelationDescriptor, RelationRegistry
from .validation import ValidationFinding, ValidationReport, derive_health, validate_bundle, validate_candidate_against_relation, validate_manifest

__version__ = "1.0.0"
