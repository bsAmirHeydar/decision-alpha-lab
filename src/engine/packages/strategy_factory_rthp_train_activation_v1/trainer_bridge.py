from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from strategy_factory_advanced_tasks_v3 import register_advanced_trainers
from strategy_factory_classical_v3 import register_classical_trainers
from strategy_factory_trainers_v3 import (
    CalibrationKind,
    CensoringSupport,
    DatasetSchema,
    DeviceKind,
    OOFProtocol,
    OrchestrationPlan,
    PredictionKind,
    PrecisionKind,
    ResourceBudget,
    SplitRole,
    TargetShape,
    TaskContract,
    TaskKind,
    TaskOrchestrator,
    TensorKind,
    TrainerConfig,
    TrainerRegistry,
    TrainingRow,
    ViewKind,
    register_reference_trainers,
)

from .canonical import sha256_material, stable_id, write_json
from .config import ActivationConfig
from .features import EncodedObservation
from .labels import CompiledLabel
from .splits import build_clustered_protocol


_KIND_MAP = {
    "binary": (TaskKind.BINARY_CLASSIFICATION, TargetShape.SCALAR, PredictionKind.PROBABILITY, "brier", False),
    "regression": (TaskKind.REGRESSION, TargetShape.SCALAR, PredictionKind.VALUE, "rmse", False),
    "ranking": (TaskKind.RANKING, TargetShape.LISTWISE, PredictionKind.RANK_SCORE, "pairwise_accuracy", True),
    "survival": (TaskKind.SURVIVAL, TargetShape.DURATION_EVENT, PredictionKind.SURVIVAL_CURVE, "survival_placeholder", True),
}


class RTHPTrainerBridge:
    def __init__(self, config: ActivationConfig, feature_order: tuple[str, ...]):
        self.config = config
        self.feature_order = feature_order

    @staticmethod
    def _registry() -> TrainerRegistry:
        registry = TrainerRegistry()
        register_reference_trainers(registry)
        register_advanced_trainers(registry)
        register_classical_trainers(registry)
        return registry

    @staticmethod
    def _trainer_for(kind: str, registry: TrainerRegistry) -> tuple[str, str, dict[str, Any]]:
        keys = {descriptor.key for descriptor in registry.snapshot()}
        preferences = {
            "binary": (
                ("uce.classical.logistic_regression", "1.0.0", {"max_iter": 1000}),
                ("uce.classical.single_feature_search", "1.0.0", {}),
                ("uce.reference.prior_binary", "1.0.0", {}),
            ),
            "regression": (
                ("uce.classical.ridge_regression", "1.0.0", {"alpha": 1.0}),
                ("uce.reference.mean_regression", "1.0.0", {}),
            ),
            "ranking": (
                ("uce.advanced.pairwise_linear_ranker", "1.0.0", {"epochs": 20, "learning_rate": 0.01, "l2": 0.001, "max_pairs_per_group": 5000}),
                ("uce.reference.linear_ranker", "1.0.0", {}),
            ),
            "survival": (
                ("uce.advanced.discrete_hazard", "1.0.0", {"horizons_ms": [900_000, 1_800_000, 3_600_000], "alpha": 1.0}),
            ),
        }
        for trainer_id, version, hyperparameters in preferences[kind]:
            if f"{trainer_id}@{version}" in keys:
                return trainer_id, version, hyperparameters
        raise ValueError(f"no registered trainer for task kind {kind}")

    def _task_contract(self, task_id: str, task_version: str, kind: str) -> TaskContract:
        task_kind, target_shape, prediction_kind, metric, maximize = _KIND_MAP[kind]
        return TaskContract(
            task_id,
            task_version,
            task_kind,
            ViewKind.TABULAR,
            target_shape,
            prediction_kind,
            metric,
            maximize,
            ("output",),
            ("negative", "positive") if kind == "binary" else (),
            censoring=CensoringSupport.RIGHT if kind == "survival" else CensoringSupport.NONE,
            sample_weight_required=False,
            calibration_required=False,
            threshold_selection_required=False,
            ranking_group_required=kind == "ranking",
        )

    def train_task(
        self,
        task: dict[str, Any],
        labels: list[CompiledLabel],
        observations: dict[str, EncodedObservation],
        output_root: Path,
    ) -> dict[str, Any]:
        task_id = task["task_id"]
        task_labels = [x for x in labels if x.task_id == task_id and x.event_id in observations]
        unique_events = {x.event_id for x in task_labels}
        if len(unique_events) < self.config.split_policy.minimum_mature_rows:
            return {
                "task_id": task_id,
                "status": "SKIPPED_INSUFFICIENT_MATURE_ROWS",
                "mature_rows": len(unique_events),
                "required_rows": self.config.split_policy.minimum_mature_rows,
            }
        if task["kind"] == "binary":
            unique_targets = {float(x.target) for x in task_labels}
            if len(unique_targets) < 2:
                return {
                    "task_id": task_id,
                    "status": "SKIPPED_SINGLE_CLASS_TARGET",
                    "mature_rows": len(unique_events),
                    "unique_target_count": len(unique_targets),
                }
        by_event = {x.event_id: x for x in task_labels}
        split_input = [(event_id, observations[event_id].event_time_ms, observations[event_id].opportunity_cluster_id) for event_id in sorted(unique_events)]
        assignments, protocol = build_clustered_protocol(split_input, self.config.split_policy, task_id)
        rows: list[TrainingRow] = []
        for event_id in sorted(unique_events, key=lambda x: (observations[x].event_time_ms, x)):
            label = by_event[event_id]
            observation = observations[event_id]
            rows.append(TrainingRow(
                event_id,
                observation.features,
                (label.target,),
                assignments[event_id],
                "fold_000" if assignments[event_id] in (SplitRole.TRAIN, SplitRole.CALIBRATION, SplitRole.THRESHOLD, SplitRole.OOF_HOLDOUT) else "final",
                observation.opportunity_cluster_id,
                observation.event_time_ms,
                max(observation.known_time_ms, label.known_time_ms),
                1.0,
                label.ranking_group if task["kind"] == "ranking" else "",
                "",
                label.censor_event,
                label.censor_duration_ms,
            ))
        dataset_material = {
            "task_id": task_id,
            "feature_order": self.feature_order,
            "rows": [
                {
                    "row_id": row.row_id,
                    "target": row.target,
                    "role": row.role.value,
                    "cluster_id": row.cluster_id,
                    "event_time_ms": row.event_time_ms,
                    "known_time_ms": row.known_time_ms,
                    "censor_event": row.censor_event,
                    "censor_duration_ms": row.censor_duration_ms,
                }
                for row in rows
            ],
        }
        dataset_hash = sha256_material(dataset_material)
        task_contract = self._task_contract(task_id, task["version"], task["kind"])
        schema = DatasetSchema(
            stable_id("rthp_dataset_", {"task": task_id, "hash": dataset_hash}, 24),
            dataset_hash,
            self.feature_order,
            ViewKind.TABULAR,
            TensorKind.DENSE_FLOAT64,
            task_contract.target_shape,
            1,
            False,
            True,
            task["kind"] == "survival",
            len(rows),
        )
        registry = self._registry()
        trainer_id, trainer_version, hyperparameters = self._trainer_for(task["kind"], registry)
        trainer = TrainerConfig(trainer_id, trainer_version, hyperparameters, self.config.resource_policy.seed, CalibrationKind.NONE)
        resources = ResourceBudget(
            self.config.resource_policy.seed,
            self.config.resource_policy.max_rows,
            self.config.resource_policy.max_features,
            16,
            self.config.resource_policy.max_memory_mb,
            self.config.resource_policy.max_wall_seconds,
            self.config.resource_policy.max_workers,
            DeviceKind.CPU,
            PrecisionKind.FLOAT64,
            True,
        )
        plan = OrchestrationPlan(
            stable_id("rthp_plan_", {"task": task_id, "dataset": dataset_hash, "trainer": trainer.key}, 24),
            "1.0.0",
            task_contract,
            trainer,
            resources,
            protocol,
            True,
            True,
            True,
            True,
        )
        result = TaskOrchestrator(registry).run(plan, schema, tuple(rows), code_hash="rthp_train_activation_v1")
        task_root = output_root / "tasks" / task_id.replace("/", "_")
        report = {
            "task_id": task_id,
            "status": "PASS",
            "kind": task["kind"],
            "label_contract_id": task["label_contract_id"],
            "row_count": len(rows),
            "independent_cluster_count": len({x.cluster_id for x in rows}),
            "dataset_id": schema.dataset_id,
            "dataset_manifest_hash": schema.dataset_manifest_hash,
            "trainer_key": trainer.key,
            "plan_hash": plan.plan_hash,
            "oof_protocol_hash": protocol.protocol_hash,
            "oof_prediction_hash": result.oof_predictions.evidence_hash,
            "final_test_prediction_hash": result.final_test_predictions.evidence_hash,
            "fold_metrics": [dict(x.metrics) for x in result.fold_trials],
            "final_metrics": dict(result.final_trial.metrics),
            "model_artifact_id": None if result.artifact_manifest is None else result.artifact_manifest.artifact_id,
            "model_state_hash": result.final_trial.model_state_hash,
            "selection_locked": result.selection_locked,
            "final_test_read_count": len([x for x in result.access_audit if x.role is SplitRole.FINAL_TEST and x.allowed]),
            "entry_treatment_execution_created": False,
        }
        report["report_digest"] = sha256_material(report)
        write_json(task_root / "task_result.json", report)
        if result.artifact_manifest is not None:
            write_json(task_root / "model_artifact_manifest.json", asdict(result.artifact_manifest))
        if result.model_card is not None:
            write_json(task_root / "model_card.json", asdict(result.model_card))
        write_json(task_root / "access_audit.json", [asdict(x) for x in result.access_audit])
        write_json(task_root / "trial_ledger.json", [asdict(x) for x in (*result.fold_trials, result.final_trial)])
        return report
