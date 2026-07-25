"""UCE-I10 deep sequence, raster, graph, regime, fusion, and qualification pack."""

from .adapters import AdapterPlan, configure_torch_determinism, probe_dependency, validate_adapter_plan
from .audit import DeterministicReplayAudit, FuturePerturbationAudit, deterministic_replay_audit, future_perturbation_audit
from .catalog import BY_FAMILY, BY_KEY, CATALOG
from .compression import distill_linear, quantize_symmetric_int8
from .contracts import *
from .enums import *
from .fusion import GatedFusion, LateWeightedFusion, StackedFusion, ablation_increment
from .gates import DeepAdmissionThresholds, evaluate_deep_admission
from .graph import GraphMessagePassingModel, MessagePassingEncoder, build_graph_artifact, remove_edges
from .qualification import qualify_deep_model
from .raster import RasterConvModel, RasterConvEncoder, audit_prefix_invariance, prefix_invariance_passes, render_chart_raster
from .regime import CusumChangeDetector, DistanceNoveltyModel, RegimeExpertGate, RegimeModel
from .registry import DeepAlgorithmRegistry
from .sequence import CausalTemporalConvModel, SequenceWindowBuilder, TemporalConvEncoder, flatten_sequence, unflatten_sequence, validate_causal_sequence
from .trainer_plugins import register_deep_trainers
from .transfer import evaluate_transfer_boundary

__all__ = [name for name in globals() if not name.startswith("_")]
