"""UCE-I10 native Trainer SDK plugins.

These plugins expose deterministic reference floors to the UCE-I07 Trainer SDK.
Optional torch/graph adapters are deliberately not registered here: they require
explicit dependency probes and phase-I10 admission evidence before scheduling.
"""

from __future__ import annotations

import json
from typing import Any, Mapping

from strategy_factory_trainers_v3.contracts import TrainerCapabilityDescriptor
from strategy_factory_trainers_v3.enums import (
    CalibrationKind,
    DeterminismLevel,
    ExportFormat,
    MissingnessSupport,
    PredictionKind,
    TargetShape,
    TaskKind,
    TensorKind,
    ViewKind,
)
from strategy_factory_trainers_v3.interfaces import FittedModel, TrainerPlugin
from strategy_factory_trainers_v3.prediction import make_batch

from .canonical import canonical_json, canonical_sha256
from .errors import DeepViewError
from .fusion import StackedFusion
from .graph import GraphMessagePassingModel
from .raster import RasterConvModel
from .regime import DistanceNoveltyModel
from .sequence import CausalTemporalConvModel


class _BaseDeepTrainer(TrainerPlugin):
    """Shared lifecycle, admission, serialization, and schema validation."""

    config: Any
    resources: Any
    task: Any
    schema: Any

    @staticmethod
    def _probability_output(task) -> bool:
        return (
            task.task_kind is TaskKind.BINARY_CLASSIFICATION
            and task.prediction_kind is PredictionKind.PROBABILITY
        )

    def configure(self, config, resources) -> None:
        if config.key != self.capability().key:
            raise DeepViewError(
                "trainer_config_key_mismatch",
                "trainer config does not match plugin capability",
                {"config": config.key, "capability": self.capability().key},
            )
        if resources.deterministic_required and self.capability().determinism is DeterminismLevel.NONDETERMINISTIC:
            raise DeepViewError("determinism_capability_mismatch", "resource budget requires deterministic training")
        self.config = config
        self.resources = resources

    def validate(self, task, schema) -> None:
        capability = self.capability()
        if task.task_kind not in capability.supported_tasks:
            raise DeepViewError("unsupported_deep_task", "task kind is not supported by trainer")
        if schema.view_kind not in capability.supported_views:
            raise DeepViewError("unsupported_deep_view", "dataset view is not supported by trainer")
        if schema.target_shape not in capability.supported_target_shapes:
            raise DeepViewError("unsupported_deep_target_shape", "target shape is not supported by trainer")
        if schema.tensor_kind not in capability.supported_tensors:
            raise DeepViewError("unsupported_deep_tensor", "tensor kind is not supported by trainer")
        if schema.row_count < capability.min_rows:
            raise DeepViewError("insufficient_deep_rows", "dataset has fewer rows than trainer minimum")
        if len(schema.feature_order) > capability.max_features:
            raise DeepViewError("deep_feature_budget_exceeded", "dataset exceeds trainer feature capability")
        if schema.has_missing_values and capability.missingness_support is MissingnessSupport.REJECT:
            raise DeepViewError("unsupported_deep_missingness", "trainer rejects missing dataset values")
        hyperparameters = self.config.hyperparameters
        if not bool(hyperparameters.get("known_time_audit_passed", False)):
            raise DeepViewError("known_time_audit_required", "known-time audit must pass before fit")
        if not bool(hyperparameters.get("future_perturbation_passed", True)):
            raise DeepViewError("future_perturbation_audit_required", "future perturbation audit must pass before fit")
        admission = str(hyperparameters.get("deep_admission_decision", "reject"))
        if admission not in ("accept", "warn"):
            raise DeepViewError("deep_admission_not_accepted", "deep admission decision does not permit training")
        self.task = task
        self.schema = schema

    def serialize(self, model: FittedModel) -> str:
        payload = {
            "state_format": "uce-i10-native-json-v1",
            "trainer_key": model.trainer_key,
            "task_key": model.task_key,
            "feature_order": model.feature_order,
            "output_names": model.output_names,
            "state": dict(model.state),
            "state_hash": model.state_hash,
        }
        return canonical_json(payload)

    def load(self, payload: str) -> FittedModel:
        parsed = json.loads(payload)
        if parsed.get("state_format") != "uce-i10-native-json-v1":
            raise DeepViewError("unsupported_deep_state_format", "model state format is unsupported")
        if canonical_sha256(parsed["state"]) != parsed["state_hash"]:
            raise DeepViewError("state_hash_mismatch", "serialized model state hash does not match")
        return FittedModel(
            parsed["trainer_key"],
            parsed["task_key"],
            tuple(parsed["feature_order"]),
            tuple(parsed["output_names"]),
            parsed["state"],
            parsed["state_hash"],
        )

    def _model(self, state: Mapping[str, Any]) -> FittedModel:
        state_hash = canonical_sha256(state)
        return FittedModel(
            self.capability().key,
            self.task.key,
            self.schema.feature_order,
            self.task.output_names,
            state,
            state_hash,
        )


class CausalTemporalConvTrainer(_BaseDeepTrainer):
    @classmethod
    def capability(cls):
        return TrainerCapabilityDescriptor(
            "uce.deep.causal_temporal_conv_ridge",
            "1.0.0",
            "deep_sequence_reference",
            (TaskKind.BINARY_CLASSIFICATION, TaskKind.REGRESSION, TaskKind.MULTI_TASK),
            (ViewKind.SEQUENCE,),
            (TargetShape.SCALAR, TargetShape.VECTOR),
            supported_tensors=(TensorKind.DENSE_FLOAT64,),
            missingness_support=MissingnessSupport.MASK_REQUIRED,
            supports_multi_output=True,
            max_outputs=64,
            calibration_kinds=(CalibrationKind.NONE, CalibrationKind.PLATT),
            export_formats=(ExportFormat.NATIVE_JSON, ExportFormat.MQL5_LINEAR),
            determinism=DeterminismLevel.BIT_EXACT,
            min_rows=8,
            tags=("causal_mask", "classical_gate_required", "reference_floor"),
        )

    def fit(self, data):
        steps = int(self.config.hyperparameters["steps"])
        channels = int(self.config.hyperparameters["channels"])
        layout = str(self.config.hyperparameters.get("layout", "time_major"))
        expected = steps * channels
        if len(data.feature_order) != expected:
            raise DeepViewError("sequence_schema_width_mismatch", "feature order does not match steps*channels")
        model = CausalTemporalConvModel.fit(
            [row.features for row in data.rows],
            [row.target for row in data.rows],
            (steps, channels),
            layout,
            alpha=float(self.config.hyperparameters.get("alpha", 0.001)),
            probability_output=self._probability_output(self.task),
            weights=[row.sample_weight for row in data.rows],
            kernel_sizes=tuple(self.config.hyperparameters.get("kernel_sizes", (2, 3))),
            dilations=tuple(self.config.hyperparameters.get("dilations", (1, 2))),
        )
        state = {
            "shape": model.shape,
            "layout": model.layout,
            "kernel_sizes": model.kernel_sizes,
            "dilations": model.dilations,
            "coefficients": model.coefficients,
            "output_count": model.output_count,
            "probability_output": model.probability_output,
        }
        return self._model(state)

    def predict(self, model, data, lineage):
        state = model.state
        native = CausalTemporalConvModel(
            tuple(state["shape"]),
            state["layout"],
            tuple(state["kernel_sizes"]),
            tuple(state["dilations"]),
            tuple(tuple(row) for row in state["coefficients"]),
            int(state["output_count"]),
            bool(state["probability_output"]),
            model.state_hash,
        )
        outputs = [native.predict(row.features) for row in data.rows]
        return make_batch(data.rows, outputs, self.task.prediction_kind, lineage, model.output_names)


class DeterministicRasterConvTrainer(_BaseDeepTrainer):
    @classmethod
    def capability(cls):
        return TrainerCapabilityDescriptor(
            "uce.deep.deterministic_chart_raster_conv",
            "1.0.0",
            "deep_vision_reference",
            (TaskKind.BINARY_CLASSIFICATION, TaskKind.REGRESSION),
            (ViewKind.IMAGE,),
            (TargetShape.SCALAR,),
            supported_tensors=(TensorKind.DENSE_FLOAT64,),
            calibration_kinds=(CalibrationKind.NONE, CalibrationKind.PLATT),
            export_formats=(ExportFormat.NATIVE_JSON, ExportFormat.MQL5_LINEAR),
            min_rows=8,
            tags=("deterministic_raster", "pixel_leakage_audit", "reference_floor"),
        )

    def fit(self, data):
        shape = tuple(int(self.config.hyperparameters[key]) for key in ("channels", "height", "width"))
        if len(data.feature_order) != shape[0] * shape[1] * shape[2]:
            raise DeepViewError("raster_schema_width_mismatch", "feature order does not match raster shape")
        model = RasterConvModel.fit(
            [row.features for row in data.rows],
            [row.target for row in data.rows],
            shape,
            float(self.config.hyperparameters.get("alpha", 0.001)),
            self._probability_output(self.task),
            [row.sample_weight for row in data.rows],
        )
        state = {
            "shape": model.shape,
            "coefficients": model.coefficients,
            "output_count": model.output_count,
            "probability_output": model.probability_output,
        }
        return self._model(state)

    def predict(self, model, data, lineage):
        state = model.state
        native = RasterConvModel(
            tuple(state["shape"]),
            tuple(tuple(row) for row in state["coefficients"]),
            int(state["output_count"]),
            bool(state["probability_output"]),
            model.state_hash,
        )
        return make_batch(
            data.rows,
            [native.predict(row.features) for row in data.rows],
            self.task.prediction_kind,
            lineage,
            model.output_names,
        )


class DeterministicGraphTrainer(_BaseDeepTrainer):
    @classmethod
    def capability(cls):
        return TrainerCapabilityDescriptor(
            "uce.deep.deterministic_graph_message_passing",
            "1.0.0",
            "deep_graph_reference",
            (TaskKind.BINARY_CLASSIFICATION, TaskKind.REGRESSION),
            (ViewKind.GRAPH,),
            (TargetShape.SCALAR,),
            calibration_kinds=(CalibrationKind.NONE, CalibrationKind.PLATT),
            export_formats=(ExportFormat.NATIVE_JSON, ExportFormat.MQL5_LINEAR),
            min_rows=8,
            tags=("topology_versioned", "node_known_time", "reference_floor"),
        )

    def fit(self, data):
        node_count = int(self.config.hyperparameters["node_count"])
        feature_count = int(self.config.hyperparameters["feature_count"])
        if len(data.feature_order) != node_count * feature_count:
            raise DeepViewError("graph_schema_width_mismatch", "feature order does not match graph shape")
        edges = tuple(
            tuple(int(value) for value in edge)
            for edge in self.config.hyperparameters.get("edges", ())
        )
        model = GraphMessagePassingModel.fit(
            [row.features for row in data.rows],
            [row.target for row in data.rows],
            node_count,
            feature_count,
            edges,
            bool(self.config.hyperparameters.get("directed", False)),
            int(self.config.hyperparameters.get("rounds", 2)),
            float(self.config.hyperparameters.get("alpha", 0.001)),
            self._probability_output(self.task),
            [row.sample_weight for row in data.rows],
        )
        state = {
            "node_count": node_count,
            "feature_count": feature_count,
            "directed": model.directed,
            "rounds": model.rounds,
            "edges": model.edges,
            "coefficients": model.coefficients,
            "output_count": model.output_count,
            "probability_output": model.probability_output,
        }
        return self._model(state)

    def predict(self, model, data, lineage):
        state = model.state
        native = GraphMessagePassingModel(
            int(state["node_count"]),
            int(state["feature_count"]),
            bool(state["directed"]),
            int(state["rounds"]),
            tuple(tuple(edge) for edge in state["edges"]),
            tuple(tuple(row) for row in state["coefficients"]),
            int(state["output_count"]),
            bool(state["probability_output"]),
            model.state_hash,
        )
        return make_batch(
            data.rows,
            [native.predict(row.features) for row in data.rows],
            self.task.prediction_kind,
            lineage,
            model.output_names,
        )


class DistanceNoveltyTrainer(_BaseDeepTrainer):
    @classmethod
    def capability(cls):
        return TrainerCapabilityDescriptor(
            "uce.deep.distance_novelty",
            "1.0.0",
            "deep_regime_novelty_reference",
            (TaskKind.NOVELTY,),
            (ViewKind.TABULAR, ViewKind.MULTI_VIEW),
            (TargetShape.SCALAR,),
            supports_sample_weight=False,
            export_formats=(ExportFormat.NATIVE_JSON, ExportFormat.MQL5_LINEAR),
            min_rows=8,
            tags=("train_only_center_scale", "abstention"),
        )

    def fit(self, data):
        model = DistanceNoveltyModel.fit(
            [row.features for row in data.rows],
            float(self.config.hyperparameters.get("quantile", 0.95)),
        )
        state = {"center": model.center, "scale": model.scale, "threshold": model.threshold}
        return self._model(state)

    def predict(self, model, data, lineage):
        state = model.state
        native = DistanceNoveltyModel(
            tuple(state["center"]),
            tuple(state["scale"]),
            float(state["threshold"]),
            model.state_hash,
        )
        outputs = [(native.score(row.features),) for row in data.rows]
        return make_batch(data.rows, outputs, PredictionKind.NOVELTY_SCORE, lineage, model.output_names)


class StackedFusionTrainer(_BaseDeepTrainer):
    @classmethod
    def capability(cls):
        return TrainerCapabilityDescriptor(
            "uce.deep.stacked_linear_fusion",
            "1.0.0",
            "deep_multi_view_reference",
            (TaskKind.BINARY_CLASSIFICATION, TaskKind.REGRESSION),
            (ViewKind.MULTI_VIEW,),
            (TargetShape.SCALAR,),
            export_formats=(ExportFormat.NATIVE_JSON, ExportFormat.MQL5_LINEAR),
            min_rows=8,
            tags=("oof_base_predictions_required", "missing_view_policy"),
        )

    def fit(self, data):
        if not bool(self.config.hyperparameters.get("oof_predictions_confirmed", False)):
            raise DeepViewError("stacking_requires_oof_predictions", "OOF base predictions must be confirmed")
        views = tuple(self.config.hyperparameters.get("view_order", data.feature_order))
        if len(views) != len(data.feature_order):
            raise DeepViewError("fusion_view_order_width_mismatch", "view order differs from feature width")
        predictions = {
            views[index]: [row.features[index] for row in data.rows]
            for index in range(len(views))
        }
        model = StackedFusion.fit(
            predictions,
            [row.target[0] for row in data.rows],
            float(self.config.hyperparameters.get("alpha", 0.001)),
            oof_predictions=True,
        )
        state = {
            "view_order": model.view_order,
            "coefficients": model.coefficients,
            "missing_policy": model.missing_policy.value,
        }
        return self._model(state)

    def predict(self, model, data, lineage):
        from .enums import MissingViewPolicy
        from .math_utils import sigmoid

        state = model.state
        native = StackedFusion(
            tuple(state["view_order"]),
            tuple(state["coefficients"]),
            MissingViewPolicy(state["missing_policy"]),
            model.state_hash,
        )
        outputs = []
        for row in data.rows:
            prediction = native.predict(
                row.row_id,
                {key: row.features[index] for index, key in enumerate(native.view_order)},
            )
            value = sigmoid(prediction.value) if self._probability_output(self.task) else prediction.value
            outputs.append((value,))
        return make_batch(data.rows, outputs, self.task.prediction_kind, lineage, model.output_names)


def register_deep_trainers(registry):
    classes = (
        CausalTemporalConvTrainer,
        DeterministicRasterConvTrainer,
        DeterministicGraphTrainer,
        DistanceNoveltyTrainer,
        StackedFusionTrainer,
    )
    for trainer in classes:
        registry.register(trainer)
    return tuple(trainer.capability().key for trainer in classes)
