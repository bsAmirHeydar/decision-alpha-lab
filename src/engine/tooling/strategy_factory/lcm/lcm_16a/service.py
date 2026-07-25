from __future__ import annotations

from pathlib import Path

from .constants import PACKAGE_RELATIVE
from .models import AuditVerificationResult
from .verify import verify_package


class LCM16AFullSystemAuditService:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root.resolve()

    def verify(self, package_root: Path | None = None) -> AuditVerificationResult:
        return verify_package(
            self.repo_root,
            (package_root or self.repo_root / PACKAGE_RELATIVE).resolve(),
        )
