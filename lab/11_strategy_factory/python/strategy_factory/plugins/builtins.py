"""Built-in plugins used by examples, tests, and simple production plans."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from ..contracts import AnatomyEvent, FeatureValue
from ..context.providers import MappingFeatureProvider
from ..decision.models import LinearModel
from .interfaces import PluginDescriptor
from .registry import PluginRegistry


@dataclass(slots=True)
class RequiredValueGate:
    descriptor: PluginDescriptor
    required_keys: tuple[str, ...]

    def evaluate(
        self,
        event: AnatomyEvent,
        context: Mapping[str, Any],
        decision_time_utc: datetime,
    ) -> tuple[bool, str | None]:
        missing = [key for key in self.required_keys if context.get(key) is None]
        if missing:
            return False, "missing_gate_values:" + ",".join(missing)
        return True, None


def register_builtins_from_spec(spec: Mapping[str, Any], registry: PluginRegistry) -> None:
    for item in spec.get("context", {}).get("providers", []):
        if item.get("implementation") != "market_state_fields":
            continue
        plugin_id = str(item["id"])
        version = str(item.get("version", "1.0.0"))
        fields = tuple(map(str, item.get("fields", ())))
        mapping = dict(item.get("mapping", {}))

        def compute(event, resolved, market_state, *, _fields=fields, _mapping=mapping):
            return {
                target: market_state.get(source)
                for target, source in ((_mapping.get(name, name), name) for name in _fields)
            }

        provider = MappingFeatureProvider(
            descriptor=PluginDescriptor(
                plugin_id=plugin_id,
                version=version,
                kind="feature_provider",
                deterministic=True,
                thread_safe=True,
                fast_path_safe=True,
                capabilities=("market_state", "online"),
            ),
            feature_names=tuple(mapping.get(name, name) for name in fields),
            compute_fn=compute,
            dependencies=tuple(map(str, item.get("dependencies", ()))),
            ttl_seconds=item.get("ttl_seconds"),
            required=bool(item.get("required", True)),
        )
        registry.register(provider)

    for item in spec.get("decision", {}).get("models", []):
        model_id = str(item["id"])
        version = str(item.get("version", "1.0.0"))
        descriptor = PluginDescriptor(
            plugin_id=model_id,
            version=version,
            kind="model",
            deterministic=True,
            thread_safe=True,
            fast_path_safe=True,
            capabilities=("predict_one", "predict_batch", "local"),
        )
        model = LinearModel(
            descriptor=descriptor,
            feature_order=tuple(map(str, item["feature_order"])),
            coefficients=tuple(float(x) for x in item["coefficients"]),
            intercept=float(item.get("intercept", 0.0)),
            output_name=str(item.get("output_name", "score")),
            logistic=bool(item.get("logistic", False)),
        )
        registry.register(model)
