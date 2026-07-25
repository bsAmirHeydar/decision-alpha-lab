from __future__ import annotations

from typing import Any

from .errors import SecurityBoundaryError

FORBIDDEN_KEY_FRAGMENTS = {
    "api_key",
    "secret",
    "password",
    "broker_token",
    "private_key",
    "signing_key",
    "order_endpoint",
    "runtime_endpoint",
}
FORBIDDEN_VALUE_FRAGMENTS = {
    "http://",
    "https://",
    "ws://",
    "wss://",
    "mt5://",
    "broker://",
}


def scan(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key).lower()
            if any(fragment in key_text for fragment in FORBIDDEN_KEY_FRAGMENTS):
                raise SecurityBoundaryError(f"forbidden key at {path}.{key}")
            scan(item, f"{path}.{key}")
        return
    if isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            scan(item, f"{path}[{index}]")
        return
    if isinstance(value, str):
        lowered = value.lower()
        if any(fragment in lowered for fragment in FORBIDDEN_VALUE_FRAGMENTS):
            raise SecurityBoundaryError(f"forbidden endpoint-like value at {path}")
