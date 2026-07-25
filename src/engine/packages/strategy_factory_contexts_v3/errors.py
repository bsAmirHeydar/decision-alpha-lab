"""Typed errors for the UCEE v3 context package SDK."""
from __future__ import annotations
from typing import Mapping, Any

class ContextSdkError(ValueError):
    def __init__(self, code: str, message: str, details: Mapping[str, Any] | None=None) -> None:
        super().__init__(message)
        self.code=code
        self.details=dict(details or {})

class ManifestError(ContextSdkError): pass
class LifecycleError(ContextSdkError): pass
class FeatureError(ContextSdkError): pass
class ViewError(ContextSdkError): pass
class ClusterError(ContextSdkError): pass
class RegistryError(ContextSdkError): pass
class ConformanceError(ContextSdkError): pass
