"""Spawn-based local worker isolation and deterministic environment capture.

The scheduler's event ordering remains sequential and deterministic, while a
worker implementation may execute its payload in a fresh spawned process.  The
spawn boundary prevents inherited mutable model state from silently affecting a
trial.  Resource claims remain governed by BudgetManager; timeout is enforced
at the parent boundary.
"""

from __future__ import annotations

import importlib
import multiprocessing as mp
import os
import platform
import sys
import time
from dataclasses import asdict, dataclass
from importlib import metadata
from typing import Any, Iterable, Mapping

from .canonical import canonical_sha256, stable_id
from .errors import ExperimentError


@dataclass(frozen=True, slots=True)
class EnvironmentCapture:
    capture_id: str
    python_version: str
    implementation: str
    platform_system: str
    platform_machine: str
    package_versions: Mapping[str, str]
    environment_flags: Mapping[str, str]
    capture_hash: str


@dataclass(frozen=True, slots=True)
class IsolatedProcessResult:
    status: str
    value: Any
    error_type: str
    error_message: str
    exit_code: int
    elapsed_seconds: float
    result_hash: str


def capture_environment(
    packages: Iterable[str] = (),
    environment_keys: Iterable[str] = ("PYTHONHASHSEED", "OMP_NUM_THREADS", "MKL_NUM_THREADS", "CUDA_VISIBLE_DEVICES"),
) -> EnvironmentCapture:
    versions: dict[str, str] = {}
    for package in sorted(set(packages)):
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = "missing"
    flags = {key: os.environ.get(key, "") for key in sorted(set(environment_keys))}
    body = {
        "python_version": platform.python_version(),
        "implementation": platform.python_implementation(),
        "platform_system": platform.system(),
        "platform_machine": platform.machine(),
        "package_versions": versions,
        "environment_flags": flags,
    }
    digest = canonical_sha256(body)
    return EnvironmentCapture(
        capture_id=stable_id("uceenv", body),
        python_version=body["python_version"],
        implementation=body["implementation"],
        platform_system=body["platform_system"],
        platform_machine=body["platform_machine"],
        package_versions=versions,
        environment_flags=flags,
        capture_hash=digest,
    )


def _resolve_callable(callable_ref: str):
    if ":" not in callable_ref:
        raise ExperimentError("invalid_callable_reference", "callable reference must be module:attribute")
    module_name, attribute_name = callable_ref.split(":", 1)
    if not module_name or not attribute_name or attribute_name.startswith("_"):
        raise ExperimentError("invalid_callable_reference", "callable reference is invalid")
    module = importlib.import_module(module_name)
    target = getattr(module, attribute_name, None)
    if not callable(target):
        raise ExperimentError("worker_callable_not_found", "worker callable does not exist or is not callable")
    return target


def _child_entry(queue, callable_ref: str, args: tuple[Any, ...], kwargs: Mapping[str, Any]) -> None:
    try:
        target = _resolve_callable(callable_ref)
        value = target(*args, **dict(kwargs))
        queue.put(("succeeded", value, "", ""))
    except BaseException as exc:  # child boundary must serialize all failures
        queue.put(("failed", None, type(exc).__name__, str(exc)))


def run_callable_in_spawn(
    callable_ref: str,
    *,
    args: tuple[Any, ...] = (),
    kwargs: Mapping[str, Any] | None = None,
    timeout_seconds: float,
) -> IsolatedProcessResult:
    if timeout_seconds <= 0:
        raise ExperimentError("invalid_process_timeout", "timeout_seconds must be positive")
    # Resolve in the parent as a fail-fast capability check before spawning.
    _resolve_callable(callable_ref)
    context = mp.get_context("spawn")
    queue = context.Queue(maxsize=1)
    process = context.Process(target=_child_entry, args=(queue, callable_ref, tuple(args), dict(kwargs or {})))
    started = time.monotonic()
    process.start()
    process.join(timeout_seconds)
    elapsed = time.monotonic() - started
    if process.is_alive():
        process.terminate()
        process.join()
        body = {
            "status": "timed_out",
            "value": None,
            "error_type": "TimeoutError",
            "error_message": "isolated worker exceeded timeout",
            "exit_code": process.exitcode if process.exitcode is not None else -1,
            "elapsed_seconds": elapsed,
        }
        return IsolatedProcessResult(result_hash=canonical_sha256(body), **body)
    if queue.empty():
        body = {
            "status": "failed",
            "value": None,
            "error_type": "ProcessExitWithoutResult",
            "error_message": "isolated worker exited without publishing a result",
            "exit_code": process.exitcode if process.exitcode is not None else -1,
            "elapsed_seconds": elapsed,
        }
        return IsolatedProcessResult(result_hash=canonical_sha256(body), **body)
    status, value, error_type, error_message = queue.get()
    body = {
        "status": status,
        "value": value,
        "error_type": error_type,
        "error_message": error_message,
        "exit_code": process.exitcode if process.exitcode is not None else 0,
        "elapsed_seconds": elapsed,
    }
    return IsolatedProcessResult(result_hash=canonical_sha256(body), **body)


def echo_value(value: Any) -> Any:
    return value


def sleep_seconds(seconds: float) -> str:
    time.sleep(seconds)
    return "done"
