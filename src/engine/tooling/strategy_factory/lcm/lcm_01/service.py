from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from . import SCANNER_VERSION
from .authority import build_permit, verify_permit
from .canonical import content_id, digest_object
from .config import SurveyConfig
from .errors import IntegrityError, SurveyError
from .finalizer import finalize_survey
from .io import atomic_publish, private_staging, read_json, write_json
from .stage_worker import STAGES


@dataclass(frozen=True)
class RunConfig:
    repo_root: Path
    destination: Path
    issued_at: str = "2026-07-18T00:00:00Z"
    survey_config: SurveyConfig = SurveyConfig()


def _verify_baseline_in_subprocess(repo: Path) -> dict:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.engine.tooling.strategy_factory.lcm.lcm_01.baseline_cli",
            "--repo-root",
            str(repo),
        ],
        cwd=repo,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise IntegrityError("LCM-00 baseline verifier returned invalid JSON") from exc
    if result.get("passed") is not True:
        raise IntegrityError("LCM-00 baseline verifier did not pass")
    return result


def _load_handoff(repo: Path) -> tuple[Path, dict]:
    roots = sorted(
        (repo / "registry/history/lcm/baselines").glob("BASELINE_*")
    )
    if not roots:
        raise IntegrityError("LCM-00 baseline package not found")
    root = roots[-1]
    handoff = read_json(root / "handoff/lcm00_to_lcm01_handoff.json")
    if handoff.get("handoff_digest") != digest_object(handoff, "handoff_digest"):
        raise IntegrityError("LCM-00 handoff digest mismatch")
    if "RUN_FORENSIC_REPOSITORY_SURVEY" not in handoff.get("allowed_actions", []):
        raise IntegrityError("LCM-00 handoff does not authorize LCM-01 survey")
    return root, handoff


def _run_stage(repo: Path, staging: Path, stage: str) -> dict:
    environment = os.environ.copy()
    existing = environment.get("PYTHONPATH", "")
    environment["PYTHONPATH"] = (
        str(repo) if not existing else str(repo) + os.pathsep + existing
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "src.engine.tooling.strategy_factory.lcm.lcm_01.stage_worker",
            "--repo-root",
            str(repo),
            "--survey-root",
            str(staging),
            "--stage",
            stage,
        ],
        cwd=repo,
        env=environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode != 0:
        raise SurveyError(
            f"LCM-01 stage failed: {stage}; stderr={completed.stderr[-4000:]}"
        )
    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SurveyError(f"LCM-01 stage returned invalid JSON: {stage}") from exc
    if result.get("passed") is not True:
        raise SurveyError(f"LCM-01 stage did not pass: {stage}")
    return result


def run_survey(cfg: RunConfig) -> Path:
    """Build and atomically publish one immutable LCM-01 survey package.

    Heavy scan stages execute in isolated child processes. This is an explicit
    repository-scale safety property: stage memory is released at process exit,
    while the parent retains only compact authority and provenance metadata.
    """

    repo = cfg.repo_root.resolve()
    destination = cfg.destination.resolve()
    if destination.exists() and any(destination.iterdir()):
        raise FileExistsError(f"destination not empty: {destination}")

    baseline_result = _verify_baseline_in_subprocess(repo)
    baseline_root, handoff = _load_handoff(repo)
    if baseline_result["baseline_id"] != handoff.get("baseline_id"):
        raise IntegrityError("baseline verifier and handoff identity mismatch")

    permit = build_permit(
        baseline_result["baseline_id"],
        baseline_result["manifest_digest"],
        handoff["handoff_digest"],
        cfg.issued_at,
    )
    verify_permit(
        permit,
        baseline_result["baseline_id"],
        baseline_result["manifest_digest"],
        handoff["handoff_digest"],
    )
    survey_material = {
        "baseline_manifest_digest": baseline_result["manifest_digest"],
        "source_handoff_digest": handoff["handoff_digest"],
        "scanner_version": SCANNER_VERSION,
        "config_digest": cfg.survey_config.digest,
    }
    survey_id = content_id("SURVEY", survey_material)
    staging = private_staging(destination.parent, ".lcm01-staging-")

    try:
        binding = {
            "schema_version": "1.0.0",
            "baseline_id": baseline_result["baseline_id"],
            "baseline_record_count": baseline_result["record_count"],
            "baseline_manifest_digest": baseline_result["manifest_digest"],
            "source_handoff_digest": handoff["handoff_digest"],
            "source_baseline_package": baseline_root.relative_to(repo).as_posix(),
            "inherited_blockers": list(handoff.get("unresolved_blockers", [])),
            "binding_digest": "",
        }
        binding["binding_digest"] = digest_object(binding, "binding_digest")
        write_json(staging / "input/lcm00_binding.json", binding)
        write_json(staging / "authority/authority_permit_snapshot.json", permit)
        config_snapshot = cfg.survey_config.to_dict()
        config_snapshot["config_digest"] = cfg.survey_config.digest
        write_json(staging / "config/survey_config_snapshot.json", config_snapshot)

        stage_results = [
            _run_stage(repo, staging, stage)
            for stage in STAGES
        ]
        write_json(
            staging / "operations/stage_worker_results.json",
            {
                "schema_version": "1.0.0",
                "phase_id": "LCM-01",
                "survey_id": survey_id,
                "stages": stage_results,
                "source_mutation_performed": False,
                "results_digest": "",
            },
        )
        worker_results = read_json(staging / "operations/stage_worker_results.json")
        worker_results["results_digest"] = digest_object(
            worker_results, "results_digest"
        )
        write_json(
            staging / "operations/stage_worker_results.json", worker_results
        )

        finalize_survey(
            staging,
            survey_id=survey_id,
            issued_at=cfg.issued_at,
            baseline_id=baseline_result["baseline_id"],
            baseline_manifest_digest=baseline_result["manifest_digest"],
            source_handoff_digest=handoff["handoff_digest"],
            inherited_blockers=list(handoff.get("unresolved_blockers", [])),
            permit=permit,
            config=cfg.survey_config,
        )

        if destination.exists() and any(destination.iterdir()):
            raise FileExistsError(f"destination not empty: {destination}")
        atomic_publish(staging, destination)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise

    return destination
