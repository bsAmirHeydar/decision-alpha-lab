from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from .canonical import digest_object

@dataclass(frozen=True)
class SurveyConfig:
    scanner_version: str = '1.0.0'
    decode_limit_bytes: int = 8_000_000
    documentation_edge_limit_per_file: int = 4000
    configuration_edge_limit_per_file: int = 2000
    duplicate_min_members: int = 2
    namespace_min_files: int = 1
    partial_superset_min_files: int = 10
    partial_superset_min_ratio_bps: int = 8000
    long_windows_path_threshold: int = 240
    include_roots: tuple[str,...] = ('mql5/Include','mql5','.')
    ignored_runtime_parts: tuple[str,...] = ('.git','.pytest_cache','__pycache__')

    def to_dict(self) -> dict:
        return {
            'schema_version':'1.0.0','scanner_version':self.scanner_version,
            'decode_limit_bytes':self.decode_limit_bytes,
            'documentation_edge_limit_per_file':self.documentation_edge_limit_per_file,
            'configuration_edge_limit_per_file':self.configuration_edge_limit_per_file,
            'duplicate_min_members':self.duplicate_min_members,
            'namespace_min_files':self.namespace_min_files,
            'partial_superset_min_files':self.partial_superset_min_files,
            'partial_superset_min_ratio_bps':self.partial_superset_min_ratio_bps,
            'long_windows_path_threshold':self.long_windows_path_threshold,
            'include_roots':list(self.include_roots),
            'ignored_runtime_parts':list(self.ignored_runtime_parts),
        }

    @property
    def digest(self) -> str:
        return digest_object(self.to_dict())
