"""Deterministic UCE-I11 experiment-manifest compiler."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any, Iterable, Mapping

from .admission import AdmissionSet, partition_candidates
from .canonical import canonical_sha256, stable_id
from .contracts import (
    CandidateAdmission,
    DagEdge,
    DagNode,
    ExperimentDeclaration,
    ExperimentManifest,
    ResourceClaim,
    TrialIdentity,
    make_trial_identity,
)
from .enums import NodeKind, ResourceDevice
from .errors import ExperimentError
from .search import SearchCandidate, propose


class ExperimentDagCompiler:
    """Compile an immutable declaration into an exact, topologically valid DAG.

    Compilation is pure: no wall clock, environment enumeration, filesystem
    state, or worker count is consulted.  Therefore the same declaration emits
    byte-identical canonical identities on every host.
    """

    def __init__(self, version: str = "1.0.0") -> None:
        self.version = version

    def compile(self, declaration: ExperimentDeclaration) -> ExperimentManifest:
        if declaration.compiler_version != self.version:
            raise ExperimentError(
                "compiler_version_mismatch",
                "declaration compiler_version differs from active compiler",
                {"declared": declaration.compiler_version, "active": self.version},
            )
        admission = partition_candidates(
            declaration.candidates,
            declaration.budget,
            require_baseline=declaration.baseline_first,
        )
        parameter_sets = self._parameter_sets(declaration, admission)
        trials, claims = self._compile_trials(declaration, admission, parameter_sets)
        nodes, edges = self._compile_nodes(declaration, admission, trials, claims)
        self._validate_dag(nodes, edges)

        payload = {
            "manifest_version": "1.0.0",
            "declaration_hash": declaration.declaration_hash,
            "compiler_version": self.version,
            "scheduler_version": declaration.scheduler_version,
            "generated_sequence": 0,
            "candidate_admission_hash": admission.evidence_hash,
            "nodes": [asdict(node) for node in nodes],
            "edges": [asdict(edge) for edge in edges],
            "trials": [asdict(trial) for trial in trials],
            "resource_claims": [asdict(claim) for claim in claims],
            "declared_trial_count": len(trials),
            "rejected_candidate_keys": [candidate.key for candidate in admission.rejected],
            "hidden_test_role": declaration.hidden_test_role,
        }
        manifest_hash = canonical_sha256(payload)
        return ExperimentManifest(
            manifest_id=stable_id("uceexpmanifest", payload),
            manifest_version="1.0.0",
            declaration_hash=declaration.declaration_hash,
            compiler_version=self.version,
            scheduler_version=declaration.scheduler_version,
            generated_sequence=0,
            candidate_admission_hash=admission.evidence_hash,
            nodes=nodes,
            edges=edges,
            trials=trials,
            resource_claims=claims,
            declared_trial_count=len(trials),
            rejected_candidate_keys=tuple(candidate.key for candidate in admission.rejected),
            hidden_test_role=declaration.hidden_test_role,
            manifest_hash=manifest_hash,
        )

    @staticmethod
    def _parameter_sets(
        declaration: ExperimentDeclaration, admission: AdmissionSet
    ) -> Mapping[str, tuple[SearchCandidate, ...]]:
        proposals = propose(declaration.search_plan)
        if not proposals:
            raise ExperimentError("search_emitted_no_candidates", "search adapter emitted no parameter candidates")
        output: dict[str, tuple[SearchCandidate, ...]] = {}
        for candidate in admission.admitted:
            if declaration.baseline_first and candidate.baseline:
                baseline = SearchCandidate(
                    ordinal=0,
                    parameter_values=dict(declaration.search_plan.baseline_parameters),
                    resource_level=declaration.search_plan.max_resource,
                    search_kind=declaration.search_plan.kind,
                    candidate_hash=canonical_sha256(
                        {
                            "candidate": candidate.key,
                            "parameters": dict(declaration.search_plan.baseline_parameters),
                            "baseline": True,
                        }
                    ),
                )
                output[candidate.key] = (baseline,)
            else:
                output[candidate.key] = proposals
        return output

    @staticmethod
    def _compile_trials(
        declaration: ExperimentDeclaration,
        admission: AdmissionSet,
        parameter_sets: Mapping[str, tuple[SearchCandidate, ...]],
    ) -> tuple[tuple[TrialIdentity, ...], tuple[ResourceClaim, ...]]:
        trials: list[TrialIdentity] = []
        claims: list[ResourceClaim] = []
        per_candidate: dict[str, int] = {}
        candidates = sorted(admission.admitted, key=lambda candidate: (not candidate.baseline, candidate.key))

        for candidate in candidates:
            per_candidate[candidate.key] = 0
            for proposal in parameter_sets[candidate.key]:
                for fold_id in declaration.folds[: declaration.budget.max_folds]:
                    for seed in declaration.seeds[: declaration.budget.max_seeds]:
                        if len(trials) >= declaration.budget.max_trials:
                            break
                        if per_candidate[candidate.key] >= declaration.budget.per_candidate_trial_cap:
                            break
                        trial = make_trial_identity(
                            declaration=declaration,
                            candidate=candidate,
                            parameter_values=proposal.parameter_values,
                            fold_id=fold_id,
                            seed=seed,
                            resource_level=proposal.resource_level,
                        )
                        wall_seconds = min(
                            candidate.estimated_wall_seconds,
                            declaration.budget.max_trial_wall_seconds,
                        )
                        memory_mb = min(candidate.estimated_memory_mb, declaration.budget.max_memory_mb)
                        claim_payload = {
                            "trial_id": trial.trial_id,
                            "device": "gpu" if candidate.requires_gpu else "cpu",
                            "cpu_slots": 1,
                            "gpu_slots": 1 if candidate.requires_gpu else 0,
                            "memory_mb": memory_mb,
                            "wall_seconds": wall_seconds,
                            "artifact_bytes": min(64 * 1024 * 1024, declaration.budget.max_artifact_bytes),
                            "deterministic_required": True,
                        }
                        claim = ResourceClaim(
                            claim_id=stable_id("uceresclaim", claim_payload),
                            trial_id=trial.trial_id,
                            device=ResourceDevice.GPU if candidate.requires_gpu else ResourceDevice.CPU,
                            cpu_slots=1,
                            gpu_slots=1 if candidate.requires_gpu else 0,
                            memory_mb=memory_mb,
                            wall_seconds=wall_seconds,
                            artifact_bytes=claim_payload["artifact_bytes"],
                            deterministic_required=True,
                        )
                        trials.append(trial)
                        claims.append(claim)
                        per_candidate[candidate.key] += 1
                    if len(trials) >= declaration.budget.max_trials or per_candidate[candidate.key] >= declaration.budget.per_candidate_trial_cap:
                        break
                if len(trials) >= declaration.budget.max_trials or per_candidate[candidate.key] >= declaration.budget.per_candidate_trial_cap:
                    break
            if len(trials) >= declaration.budget.max_trials:
                break

        if not trials:
            raise ExperimentError("budget_emitted_zero_trials", "budget/search axes emitted zero trials")
        if len({trial.trial_id for trial in trials}) != len(trials):
            raise ExperimentError("trial_identity_collision", "compiled trial identities collided")
        return tuple(trials), tuple(claims)

    @staticmethod
    def _compile_nodes(
        declaration: ExperimentDeclaration,
        admission: AdmissionSet,
        trials: tuple[TrialIdentity, ...],
        claims: tuple[ResourceClaim, ...],
    ) -> tuple[tuple[DagNode, ...], tuple[DagEdge, ...]]:
        nodes: list[DagNode] = []
        edges: list[DagEdge] = []
        node_by_semantic: dict[str, str] = {}

        def add_node(
            kind: NodeKind,
            semantic_key: str,
            payload: Mapping[str, Any],
            dependencies: Iterable[str],
            priority: int,
            *,
            claim_hash: str = "",
            trial_id: str = "",
        ) -> str:
            dependency_tuple = tuple(dependencies)
            node_payload = {
                "kind": kind.value,
                "semantic_key": semantic_key,
                "payload": dict(payload),
                "dependencies": dependency_tuple,
                "priority": priority,
                "resource_claim_hash": claim_hash,
                "trial_id": trial_id,
            }
            node_id = stable_id("ucedagnode", node_payload)
            node = DagNode(
                node_id=node_id,
                kind=kind,
                semantic_key=semantic_key,
                payload_hash=canonical_sha256(payload),
                dependencies=dependency_tuple,
                priority=priority,
                resource_claim_hash=claim_hash,
                trial_id=trial_id,
            )
            nodes.append(node)
            node_by_semantic[semantic_key] = node_id
            for parent_id in dependency_tuple:
                edges.append(DagEdge(parent_id, node_id))
            return node_id

        dataset = add_node(
            NodeKind.DATASET,
            f"dataset:{declaration.dataset_id}",
            {"dataset_id": declaration.dataset_id, "manifest_hash": declaration.dataset_manifest_hash},
            (),
            0,
        )
        split = add_node(
            NodeKind.SPLIT,
            f"split:{declaration.split_plan_id}",
            {
                "split_plan_id": declaration.split_plan_id,
                "split_plan_hash": declaration.split_plan_hash,
                "requested_roles": declaration.requested_roles,
                "hidden_test_role": declaration.hidden_test_role,
            },
            (dataset,),
            1,
        )
        transform = add_node(
            NodeKind.TRANSFORM,
            f"transform:{declaration.transform_plan_hash[:16]}",
            {
                "transform_plan_hash": declaration.transform_plan_hash,
                "known_time_policy_hash": declaration.known_time_policy_hash,
            },
            (split,),
            2,
        )

        trainer_nodes: dict[str, str] = {}
        for index, candidate in enumerate(sorted(admission.admitted, key=lambda item: (not item.baseline, item.key))):
            trainer_nodes[candidate.key] = add_node(
                NodeKind.TRAINER,
                f"trainer:{candidate.key}",
                {
                    "candidate_key": candidate.key,
                    "trainer_key": candidate.trainer_key,
                    "admission_hash": candidate.admission_hash,
                    "baseline": candidate.baseline,
                    "capability_flags": dict(candidate.capability_flags),
                },
                (transform,),
                10 + index,
            )

        claim_by_trial = {claim.trial_id: claim for claim in claims}
        candidate_by_key = {candidate.key: candidate for candidate in admission.admitted}
        terminal_validation_nodes: list[str] = []
        export_nodes: list[str] = []

        for ordinal, trial in enumerate(trials):
            candidate = candidate_by_key[trial.candidate_key]
            base_priority = 100 if candidate.baseline else 1000
            base_priority += ordinal
            trainer = trainer_nodes[trial.candidate_key]
            claim = claim_by_trial[trial.trial_id]
            trial_node = add_node(
                NodeKind.TRIAL,
                f"trial:{trial.trial_id}",
                {"identity_hash": trial.identity_hash, "parameter_values": dict(trial.parameter_values)},
                (trainer,),
                base_priority,
                claim_hash=claim.claim_hash,
                trial_id=trial.trial_id,
            )
            fold_node = add_node(
                NodeKind.FOLD,
                f"fold:{trial.trial_id}:{trial.fold_id}",
                {"fold_id": trial.fold_id, "split_plan_hash": trial.split_plan_hash},
                (trial_node,),
                base_priority + 1,
                trial_id=trial.trial_id,
            )
            seed_node = add_node(
                NodeKind.SEED,
                f"seed:{trial.trial_id}:{trial.seed}",
                {"seed": trial.seed, "resource_level": trial.resource_level},
                (fold_node,),
                base_priority + 2,
                trial_id=trial.trial_id,
            )
            calibration_nodes: list[str] = []
            for calibration in declaration.calibration_kinds:
                calibration_nodes.append(
                    add_node(
                        NodeKind.CALIBRATION,
                        f"calibration:{trial.trial_id}:{calibration}",
                        {"kind": calibration, "fold_id": trial.fold_id},
                        (seed_node,),
                        base_priority + 3,
                        trial_id=trial.trial_id,
                    )
                )
            threshold_nodes: list[str] = []
            for calibration_node, calibration in zip(calibration_nodes, declaration.calibration_kinds):
                for threshold in declaration.threshold_kinds:
                    threshold_nodes.append(
                        add_node(
                            NodeKind.THRESHOLD,
                            f"threshold:{trial.trial_id}:{calibration}:{threshold}",
                            {"kind": threshold, "calibration": calibration},
                            (calibration_node,),
                            base_priority + 4,
                            trial_id=trial.trial_id,
                        )
                    )
            validation = add_node(
                NodeKind.VALIDATION,
                f"validation:{trial.trial_id}",
                {
                    "requested_roles": declaration.requested_roles,
                    "hidden_role_excluded": declaration.hidden_test_role,
                    "target_plan_hash": declaration.target_plan_hash,
                    "economics_plan_hash": declaration.economics_plan_hash,
                },
                tuple(threshold_nodes),
                base_priority + 5,
                trial_id=trial.trial_id,
            )
            terminal_validation_nodes.append(validation)
            if declaration.export_requested:
                export_nodes.append(
                    add_node(
                        NodeKind.EXPORT,
                        f"export:{trial.trial_id}",
                        {"candidate_key": trial.candidate_key, "trial_identity_hash": trial.identity_hash},
                        (validation,),
                        base_priority + 6,
                        trial_id=trial.trial_id,
                    )
                )

        ensemble_nodes: list[str] = []
        for ensemble in declaration.ensemble_kinds:
            ensemble_nodes.append(
                add_node(
                    NodeKind.ENSEMBLE,
                    f"ensemble:{ensemble}",
                    {"kind": ensemble, "base_trial_count": len(terminal_validation_nodes)},
                    tuple(terminal_validation_nodes),
                    100000,
                )
            )
        report_dependencies = tuple(ensemble_nodes or terminal_validation_nodes)
        report = add_node(
            NodeKind.REPORT,
            f"report:{declaration.experiment_id}",
            {
                "experiment_id": declaration.experiment_id,
                "declared_trial_count": len(trials),
                "rejected_candidate_keys": tuple(candidate.key for candidate in admission.rejected),
            },
            report_dependencies,
            200000,
        )
        if export_nodes:
            # Report existence is required by export publication, but model export
            # nodes themselves remain trial-local and do not depend on selection.
            add_node(
                NodeKind.EXPORT,
                f"export-index:{declaration.experiment_id}",
                {"trial_export_count": len(export_nodes)},
                tuple(export_nodes) + (report,),
                200001,
            )
        return tuple(nodes), tuple(edges)

    @staticmethod
    def _validate_dag(nodes: tuple[DagNode, ...], edges: tuple[DagEdge, ...]) -> None:
        node_ids = {node.node_id for node in nodes}
        if any(edge.parent_id not in node_ids or edge.child_id not in node_ids for edge in edges):
            raise ExperimentError("dangling_dag_edge", "DAG contains edge to unknown node")
        adjacency: dict[str, list[str]] = {node_id: [] for node_id in node_ids}
        indegree: dict[str, int] = {node_id: 0 for node_id in node_ids}
        for edge in edges:
            adjacency[edge.parent_id].append(edge.child_id)
            indegree[edge.child_id] += 1
        ready = sorted(node_id for node_id, degree in indegree.items() if degree == 0)
        visited = 0
        while ready:
            node_id = ready.pop(0)
            visited += 1
            for child in sorted(adjacency[node_id]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
                    ready.sort()
        if visited != len(nodes):
            raise ExperimentError("dag_cycle_detected", "compiled experiment graph contains a cycle")


def manifest_semantic_snapshot(manifest: ExperimentManifest) -> dict[str, Any]:
    """Return the exact content used by reproducibility comparisons."""
    return {
        "declaration_hash": manifest.declaration_hash,
        "compiler_version": manifest.compiler_version,
        "scheduler_version": manifest.scheduler_version,
        "candidate_admission_hash": manifest.candidate_admission_hash,
        "nodes": [asdict(node) for node in manifest.nodes],
        "edges": [asdict(edge) for edge in manifest.edges],
        "trials": [asdict(trial) for trial in manifest.trials],
        "resource_claims": [asdict(claim) for claim in manifest.resource_claims],
        "rejected_candidate_keys": manifest.rejected_candidate_keys,
        "hidden_test_role": manifest.hidden_test_role,
    }
