"""Lazy dependency and adapter boundaries for optional deep implementations.

Importing the base package never imports torch, torch_geometric, onnx, or
hmmlearn. Optional adapters must probe capabilities first and produce evidence
that can be retained even when a dependency is missing or incompatible.
"""

from __future__ import annotations

import importlib
import importlib.metadata
from dataclasses import dataclass
from typing import Mapping

from .canonical import canonical_sha256
from .contracts import DependencyProbe
from .enums import DependencyStatus
from .errors import DeepViewError


@dataclass(frozen=True, slots=True)
class AdapterPlan:
    algorithm_key: str
    dependency_profile: str
    required_modules: Mapping[str, str]
    deterministic_required: bool
    seed: int
    device: str = "cpu"
    precision: str = "float32"
    export_format: str = "onnx"

    @property
    def plan_hash(self) -> str:
        return canonical_sha256(self)


def _version_tuple(value: str) -> tuple[int, ...]:
    digits = []
    for piece in value.split("."):
        numeric = "".join(character for character in piece if character.isdigit())
        if not numeric:
            break
        digits.append(int(numeric))
    return tuple(digits)


def probe_dependency(profile: str, module: str, minimum_version: str) -> DependencyProbe:
    try:
        importlib.import_module(module)
    except Exception as exc:  # dependency probing must retain the precise failure
        material = {
            "profile": profile,
            "module": module,
            "status": DependencyStatus.MISSING.value,
            "minimum_version": minimum_version,
            "reason": type(exc).__name__,
        }
        return DependencyProbe(
            profile,
            module,
            DependencyStatus.MISSING,
            "",
            minimum_version,
            f"{type(exc).__name__}: {exc}",
            canonical_sha256(material),
        )
    try:
        detected = importlib.metadata.version(module.replace("_", "-"))
    except importlib.metadata.PackageNotFoundError:
        detected = getattr(importlib.import_module(module), "__version__", "unknown")
    compatible = detected == "unknown" or _version_tuple(detected) >= _version_tuple(minimum_version)
    status = DependencyStatus.AVAILABLE if compatible else DependencyStatus.INCOMPATIBLE
    reason = "dependency available" if compatible else "detected version is below the required minimum"
    material = {
        "profile": profile,
        "module": module,
        "status": status.value,
        "detected_version": detected,
        "minimum_version": minimum_version,
        "reason": reason,
    }
    return DependencyProbe(
        profile,
        module,
        status,
        detected,
        minimum_version,
        reason,
        canonical_sha256(material),
    )


def validate_adapter_plan(plan: AdapterPlan) -> tuple[DependencyProbe, ...]:
    if not plan.algorithm_key or not plan.dependency_profile:
        raise DeepViewError("invalid_adapter_plan", "algorithm key and dependency profile are required")
    if plan.device not in ("cpu", "cuda"):
        raise DeepViewError("unsupported_adapter_device", "adapter device must be cpu or cuda")
    if plan.precision not in ("float32", "float64"):
        raise DeepViewError("unsupported_adapter_precision", "adapter precision must be float32 or float64")
    probes = tuple(
        probe_dependency(plan.dependency_profile, module, minimum)
        for module, minimum in sorted(plan.required_modules.items())
    )
    failed = [probe for probe in probes if probe.status is not DependencyStatus.AVAILABLE]
    if failed:
        raise DeepViewError(
            "optional_dependency_unavailable",
            "one or more optional adapter dependencies are unavailable",
            {"probes": [probe.module + ":" + probe.status.value for probe in failed]},
        )
    return probes


def configure_torch_determinism(seed: int) -> Mapping[str, object]:
    """Configure deterministic torch behavior after a successful probe.

    This function is isolated so the base package remains dependency-free.
    """

    torch = importlib.import_module("torch")
    torch.manual_seed(int(seed))
    if hasattr(torch, "cuda") and torch.cuda.is_available():
        torch.cuda.manual_seed_all(int(seed))
    if hasattr(torch, "use_deterministic_algorithms"):
        torch.use_deterministic_algorithms(True)
    if hasattr(torch, "backends") and hasattr(torch.backends, "cudnn"):
        torch.backends.cudnn.benchmark = False
        torch.backends.cudnn.deterministic = True
    return {
        "seed": int(seed),
        "torch_version": getattr(torch, "__version__", "unknown"),
        "deterministic_algorithms": True,
        "cuda_available": bool(torch.cuda.is_available()) if hasattr(torch, "cuda") else False,
    }
