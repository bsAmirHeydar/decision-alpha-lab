from __future__ import annotations

import json
import os
import shutil
from dataclasses import asdict
from pathlib import Path
from typing import Any

from tools.repository_paths import RepositoryPaths, find_repository_root, migrated_relative_path

from .canonical import canonical_json, sha256_file, sha256_material, write_json, write_jsonl
from .config import ActivationConfig
from .features import EncodedObservation, RTHPFeatureEncoder
from .labels import RTHPLabelCompiler, read_jsonl
from .materializer import MaterializationResult, RTHPHistoricalMaterializer
from .m1_materializer import RTHPM1HistoricalMaterializer
from .trainer_bridge import RTHPTrainerBridge


PACKAGE_VERSION = "1.0.0"


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _write_hash_ledger(root: Path, output: Path) -> dict[str, str]:
    rows: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path == output:
            continue
        rel = path.relative_to(root).as_posix()
        rows[rel] = sha256_file(path)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("".join(f"sha256:{digest}  {rel}\n" for rel, digest in rows.items()), encoding="utf-8", newline="\n")
    return rows


def verify_run_root(run_root: str | Path) -> dict[str, Any]:
    root = Path(run_root).resolve()
    manifest_path = root / "run_manifest.json"
    ledger_path = root / "RUN_FILE_HASHES.sha256"
    marker_path = root / "RUN_COMPLETE"
    if not manifest_path.is_file() or not ledger_path.is_file() or not marker_path.is_file():
        raise ValueError("run root is incomplete")
    errors: list[str] = []
    verified = 0
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        prefix, rel = line.split("  ", 1)
        if not prefix.startswith("sha256:"):
            errors.append(f"invalid ledger line: {line}")
            continue
        path = root / rel
        if not path.is_file():
            errors.append(f"missing: {rel}")
            continue
        actual = sha256_file(path)
        expected = prefix.removeprefix("sha256:")
        if actual != expected:
            errors.append(f"hash mismatch: {rel}")
        else:
            verified += 1
    manifest = _read_json(manifest_path)
    if manifest.get("status") not in {"PASS", "PASS_WITH_SKIPS"}:
        errors.append(f"unexpected run status: {manifest.get('status')}")
    return {
        "status": "PASS" if not errors else "FAIL",
        "run_root": root.as_posix(),
        "verified_file_count": verified,
        "errors": errors,
        "run_id": manifest.get("run_id"),
        "run_digest": manifest.get("run_digest"),
    }


class RTHPTrainActivationPipeline:
    """Context-owned one-shot activation over immutable local source artifacts.

    The class performs only RTHP-specific materialization and contract binding.
    Feature compilation and model training are delegated to existing Strategy
    Factory engines. It never mutates canonical Context or shared engine files.
    """

    def __init__(self, config: ActivationConfig, repository_root: Path | None = None):
        self.config = config
        root = repository_root or find_repository_root(__file__)
        self.paths = RepositoryPaths.from_root(root)
        self.repository_root = self.paths.root
        generated = self.paths.generated_context("rthp_cross_symbol_cycle_divergence")
        authored = self.paths.authored_context("CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1")
        self.ai_input_root = generated / "ai_input"
        self.task_registry_path = self.ai_input_root / "task_references.v1.json"
        self.label_bindings_path = self.ai_input_root / "label_bindings.v1.json"
        self.context_manifest_path = authored / "context_manifest.yaml"
        self.acl03_receipt_path = authored / "generated/acl_03/compiled/compilation_receipt.json"
        self._validate_repository_inputs()

    def _validate_repository_inputs(self) -> None:
        for path in (
            self.task_registry_path,
            self.label_bindings_path,
            self.context_manifest_path,
            self.acl03_receipt_path,
        ):
            if not path.is_file():
                raise FileNotFoundError(path)
        context_text = self.context_manifest_path.read_text(encoding="utf-8")
        if "context_version: 1.0.2" not in context_text:
            raise ValueError("RTHP canonical Context 1.0.2 is required")
        output = self.config.output_root.resolve()
        logical_output = output
        try:
            relative_output = output.relative_to(self.repository_root.resolve())
        except ValueError:
            relative_output = None
        if relative_output is not None:
            logical_output = self.repository_root / migrated_relative_path(self.repository_root, relative_output)
        protected = (
            self.paths.context_root,
            self.paths.source_root,
            self.paths.registry_root,
            self.paths.schema_root,
            self.paths.release_root,
        )
        for root in protected:
            try:
                logical_output.relative_to(root.resolve())
            except ValueError:
                continue
            raise ValueError(f"run output must not be written into a protected source tree: {output}")
        try:
            output.relative_to(self.repository_root.resolve())
        except ValueError:
            return
        allowed = self.paths.runtime_run_root.resolve()
        try:
            output.relative_to(allowed)
        except ValueError as exc:
            raise ValueError(f"repository-local run output must be under {allowed}") from exc

    @property
    def source_snapshot(self) -> dict[str, Any]:
        source = self.config.data_source
        return {
            "schema_version": "1.0.0",
            "provider": source.provider,
            "primary_symbol": source.primary_symbol,
            "secondary_symbol": source.secondary_symbol,
            "source_mode": source.mode,
            "primary_source_uri": source.source_paths[0].resolve().as_uri(),
            "secondary_source_uri": source.source_paths[1].resolve().as_uri(),
            "primary_content_hash": "sha256:" + sha256_file(source.source_paths[0]),
            "secondary_content_hash": "sha256:" + sha256_file(source.source_paths[1]),
            "timezone": source.timezone,
            "price_basis": source.price_basis,
            "tick_size_source": source.tick_size_source,
            "contract_roll_policy": source.contract_roll_policy,
            "entitlement_id": source.entitlement_id,
            "producer_version": source.producer_version,
            "availability_time_policy": source.availability_time_policy,
            "source_revision": source.source_revision,
            "start_time_ms": source.start_time_ms,
            "end_time_ms": source.end_time_ms,
        }

    def _staging_root(self) -> Path:
        final = self.config.output_root.resolve()
        return final.parent / f".{final.name}.staging.{os.getpid()}"

    def _prepare_staging(self) -> Path:
        final = self.config.output_root.resolve()
        if final.exists():
            raise FileExistsError(f"run output already exists: {final}")
        staging = self._staging_root()
        if staging.exists():
            shutil.rmtree(staging)
        staging.mkdir(parents=True, exist_ok=False)
        return staging

    @staticmethod
    def _feature_row(observation: EncodedObservation) -> dict[str, Any]:
        return {
            "event_id": observation.event_id,
            "observation_id": observation.observation_id,
            "observation_hash": observation.observation_hash,
            "opportunity_cluster_id": observation.opportunity_cluster_id,
            "event_time_ms": observation.event_time_ms,
            "known_time_ms": observation.known_time_ms,
            "feature_order": list(observation.feature_order),
            "features": list(observation.features),
            "view_hashes": observation.view_hashes,
        }

    def _compile_features(self, occurrences: list[dict[str, Any]], staging: Path) -> tuple[dict[str, EncodedObservation], dict[str, Any]]:
        encoder = RTHPFeatureEncoder()
        observations: dict[str, EncodedObservation] = {}
        for source in occurrences:
            encoded = encoder.compile(source, retain_views=self.config.retain_materialized_views)
            if encoded.event_id in observations:
                raise ValueError(f"duplicate event_id during feature compilation: {encoded.event_id}")
            observations[encoded.event_id] = encoded
        rows = [self._feature_row(observations[key]) for key in sorted(observations)]
        feature_path = staging / "datasets" / "rthp_feature_matrix.jsonl"
        write_jsonl(feature_path, rows)
        report = {
            "report_id": "RTHP_FEATURE_MATERIALIZATION_V1",
            "schema_version": "1.0.0",
            "status": "PASS" if rows else "BLOCKED",
            "row_count": len(rows),
            "feature_count": len(encoder.feature_order),
            "feature_order": list(encoder.feature_order),
            "independent_cluster_count": len({x.opportunity_cluster_id for x in observations.values()}),
            "view_ids": sorted({view_id for row in observations.values() for view_id in row.view_hashes}),
            "engine_modified": False,
            "canonical_context_modified": False,
        }
        report["report_digest"] = sha256_material(report)
        write_json(staging / "reports" / "feature_materialization_report.json", report)
        return observations, report

    def _compile_labels(
        self,
        materialization: MaterializationResult,
        staging: Path,
    ) -> tuple[list[Any], dict[str, Any]]:
        compiler = RTHPLabelCompiler(self.task_registry_path, self.label_bindings_path)
        occurrences = read_jsonl(materialization.occurrence_ledger)
        reference_states = read_jsonl(materialization.reference_state_ledger)
        role_paths = read_jsonl(materialization.role_price_path_ledger)
        labels, stats = compiler.compile(occurrences, reference_states, role_paths, self.config.selected_task_ids)
        label_rows = [asdict(label) for label in labels]
        write_jsonl(staging / "datasets" / "rthp_label_matrix.jsonl", label_rows)
        report = {
            "report_id": "RTHP_LABEL_MATERIALIZATION_V1",
            "schema_version": "1.0.0",
            "status": "PASS" if labels else "BLOCKED",
            "label_row_count": len(labels),
            "task_count_with_mature_labels": len({x.task_id for x in labels}),
            "task_statistics": stats,
            "labels_are_post_cut_only": True,
            "unmatured_labels_excluded": True,
            "entry_treatment_execution_created": False,
        }
        report["report_digest"] = sha256_material(report)
        write_json(staging / "reports" / "label_materialization_report.json", report)
        return labels, report

    def _selected_tasks(self) -> list[dict[str, Any]]:
        tasks = _read_json(self.task_registry_path)["tasks"]
        selected = set(self.config.selected_task_ids)
        if selected:
            missing = selected.difference({x["task_id"] for x in tasks})
            if missing:
                raise ValueError(f"unknown selected task ids: {sorted(missing)}")
            tasks = [x for x in tasks if x["task_id"] in selected]
        elif not self.config.train_all_mature_tasks:
            raise ValueError("selected_task_ids must be provided when train_all_mature_tasks is false")
        return sorted(tasks, key=lambda x: x["task_id"])

    def _batch_manifest(
        self,
        staging: Path,
        materialization: MaterializationResult,
        feature_report: dict[str, Any],
        label_report: dict[str, Any],
        tasks: list[dict[str, Any]],
    ) -> dict[str, Any]:
        artifacts = {
            "occurrence_ledger": "sha256:" + sha256_file(materialization.occurrence_ledger),
            "reference_state_ledger": "sha256:" + sha256_file(materialization.reference_state_ledger),
            "cycle_instance_ledger": "sha256:" + sha256_file(materialization.cycle_instance_ledger),
            "role_price_path_ledger": "sha256:" + sha256_file(materialization.role_price_path_ledger),
            "data_binding": "sha256:" + sha256_file(materialization.data_binding),
            "feature_matrix": "sha256:" + sha256_file(staging / "datasets" / "rthp_feature_matrix.jsonl"),
            "label_matrix": "sha256:" + sha256_file(staging / "datasets" / "rthp_label_matrix.jsonl"),
            "task_registry": "sha256:" + sha256_file(self.task_registry_path),
            "label_bindings": "sha256:" + sha256_file(self.label_bindings_path),
        }
        manifest = {
            "batch_id": f"RTHP_IMMUTABLE_RESEARCH_BATCH_{self.config.run_id}",
            "schema_version": "1.0.0",
            "status": "FROZEN",
            "run_id": self.config.run_id,
            "context_id": "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1",
            "context_version": "1.0.2",
            "context_package_key": "rthp.cross_symbol_cycle_divergence@1.0.0",
            "config_digest": self.config.config_digest,
            "source_snapshot": self.source_snapshot,
            "artifact_hashes": artifacts,
            "selected_tasks": tasks,
            "feature_report_digest": feature_report["report_digest"],
            "label_report_digest": label_report["report_digest"],
            "split_policy": asdict(self.config.split_policy),
            "resource_policy": asdict(self.config.resource_policy),
            "final_test_sealed": True,
            "network_fetch_allowed": False,
            "engine_modified": False,
            "canonical_context_modified": False,
            "entry_treatment_execution_created": False,
        }
        manifest["batch_digest"] = sha256_material(manifest)
        write_json(staging / "batch" / "immutable_batch_manifest.json", manifest)
        return manifest

    def _train(
        self,
        staging: Path,
        labels: list[Any],
        observations: dict[str, EncodedObservation],
        tasks: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not observations:
            return []
        feature_order = next(iter(observations.values())).feature_order
        bridge = RTHPTrainerBridge(self.config, feature_order)
        results: list[dict[str, Any]] = []
        for task in tasks:
            result = bridge.train_task(task, labels, observations, staging)
            results.append(result)
            if result["status"].startswith("SKIPPED") and self.config.fail_on_task_insufficiency:
                raise RuntimeError(f"task failed minimum-data gate: {task['task_id']}")
        return results

    def run(self) -> dict[str, Any]:
        staging = self._prepare_staging()
        final = self.config.output_root.resolve()
        try:
            write_json(staging / "source_snapshot.json", self.source_snapshot)
            write_json(staging / "activation_config.normalized.json", asdict(self.config))
            materializer = RTHPM1HistoricalMaterializer(self.config) if self.config.data_source.mode == "PAIRED_M1_BAR_JSONL" else RTHPHistoricalMaterializer(self.config)
            materialization = materializer.materialize(staging)
            if materialization.occurrence_count == 0:
                raise RuntimeError("no confirmed RTHP occurrences were materialized")
            occurrences = read_jsonl(materialization.occurrence_ledger)
            observations, feature_report = self._compile_features(occurrences, staging)
            labels, label_report = self._compile_labels(materialization, staging)
            tasks = self._selected_tasks()
            batch = self._batch_manifest(staging, materialization, feature_report, label_report, tasks)
            task_results = self._train(staging, labels, observations, tasks)
            passed = [x for x in task_results if x["status"] == "PASS"]
            skipped = [x for x in task_results if x["status"].startswith("SKIPPED")]
            status = "PASS" if passed and not skipped else "PASS_WITH_SKIPS" if passed else "BLOCKED"
            summary = {
                "report_id": "RTHP_REAL_TRAIN_ACTIVATION_V1",
                "schema_version": "1.0.0",
                "status": status,
                "run_id": self.config.run_id,
                "context_id": "CTX_RTHP_CROSS_SYMBOL_CYCLE_DIVERGENCE_V1",
                "context_version": "1.0.2",
                "context_package_key": "rthp.cross_symbol_cycle_divergence@1.0.0",
                "source_digest": materialization.source_digest,
                "config_digest": self.config.config_digest,
                "batch_digest": batch["batch_digest"],
                "occurrence_count": materialization.occurrence_count,
                "feature_row_count": len(observations),
                "label_row_count": len(labels),
                "requested_task_count": len(tasks),
                "passed_task_count": len(passed),
                "skipped_task_count": len(skipped),
                "failed_task_count": len([x for x in task_results if x["status"] not in {"PASS"} and not x["status"].startswith("SKIPPED")]),
                "task_results": task_results,
                "engine_modified": False,
                "canonical_context_modified": False,
                "entry_treatment_execution_created": False,
                "capital_authority_created": False,
                "network_fetch_used": False,
                "final_test_sealed": True,
            }
            summary["run_digest"] = sha256_material(summary)
            write_json(staging / "reports" / "train_activation_report.json", summary)
            write_json(staging / "run_manifest.json", summary)
            _write_hash_ledger(staging, staging / "RUN_FILE_HASHES.sha256")
            (staging / "RUN_COMPLETE").write_text(summary["run_digest"] + "\n", encoding="utf-8", newline="\n")
            staging.replace(final)
            verification = verify_run_root(final)
            if verification["status"] != "PASS":
                raise RuntimeError("post-commit run verification failed: " + "; ".join(verification["errors"]))
            return summary
        except Exception:
            if staging.exists():
                failure_root = staging.parent / f"{staging.name}.failed"
                if failure_root.exists():
                    shutil.rmtree(failure_root)
                staging.replace(failure_root)
            raise
