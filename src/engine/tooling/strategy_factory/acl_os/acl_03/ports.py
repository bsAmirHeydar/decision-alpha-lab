from __future__ import annotations
from pathlib import Path
from typing import Any, Protocol, runtime_checkable

@runtime_checkable
class DomainLinterPort(Protocol):
    extension_id: str
    def lint(self, package:dict[str,Any])->list[dict[str,Any]]: ...

@runtime_checkable
class AdapterContractProviderPort(Protocol):
    extension_id: str
    def contracts(self, package:dict[str,Any])->list[dict[str,Any]]: ...

@runtime_checkable
class GoldenCaseProviderPort(Protocol):
    extension_id: str
    def cases(self, context_root:Path, package:dict[str,Any])->list[dict[str,Any]]: ...

@runtime_checkable
class ArtifactPublisherPort(Protocol):
    def publish(self, output_root:Path, artifacts:list[dict[str,Any]])->dict[str,Any]: ...
