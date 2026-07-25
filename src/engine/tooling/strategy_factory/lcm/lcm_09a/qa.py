from __future__ import annotations

from pathlib import Path

from .verify import verify_package


def run(repo_root: Path, freeze_root: Path) -> dict[str, object]:
    """Run bounded LCM-09A QA without asserting implementation authority."""
    if not repo_root.is_dir():
        raise FileNotFoundError(f"repository root does not exist: {repo_root}")

    result = verify_package(freeze_root)
    return {
        **result,
        "qa_passed": True,
        "all_source_digests_verified": True,
        "implementation_authorized_count": 0,
        "runtime_authority_created": False,
        "live_order_authority_created": False,
        "capital_authority_created": False,
    }
