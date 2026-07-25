"""Artifact classification and bounded ownership heuristics."""
from __future__ import annotations

import mimetypes
from pathlib import Path

from .constants import (
    ARCHIVE_SUFFIXES,
    BINARY_SUFFIXES,
    CRITICAL_DOMAIN_PATTERNS,
    DOCUMENT_SUFFIXES,
    SCHEMA_SUFFIXES,
    SOURCE_SUFFIXES,
)


def _contains_any(text: str, tokens: tuple[str, ...] | set[str]) -> bool:
    lowered = text.lower()
    return any(token.lower() in lowered for token in tokens)


def detect_language(path: Path) -> str | None:
    suffix = path.suffix.lower()
    return {
        ".py": "python", ".pyi": "python", ".mq5": "mql5", ".mqh": "mql5",
        ".ps1": "powershell", ".psm1": "powershell", ".sh": "shell",
        ".bat": "batch", ".cmd": "batch", ".js": "javascript", ".jsx": "javascript",
        ".ts": "typescript", ".tsx": "typescript", ".cpp": "cpp", ".cc": "cpp",
        ".c": "c", ".h": "c_header", ".hpp": "cpp_header", ".sql": "sql",
        ".md": "markdown", ".rst": "rst", ".yaml": "yaml", ".yml": "yaml",
        ".json": "json", ".jsonl": "jsonl", ".toml": "toml", ".xml": "xml",
        ".xsd": "xsd", ".proto": "protobuf", ".csv": "csv", ".canvas": "obsidian_canvas",
    }.get(suffix)


def classify_category(rel_path: str) -> str:
    path = Path(rel_path)
    suffix = path.suffix.lower()
    lower = rel_path.lower()
    name = path.name.lower()
    if suffix in SOURCE_SUFFIXES:
        return "source_code"
    if suffix in DOCUMENT_SUFFIXES:
        return "documentation"
    if suffix in ARCHIVE_SUFFIXES:
        return "archive_or_release_bundle"
    if suffix in BINARY_SUFFIXES:
        return "binary_or_model"
    if lower.startswith("schemas/") or "/schemas/" in lower or name.endswith(".schema.json"):
        return "schema"
    if lower.startswith("policies/") or "/policies/" in lower:
        return "policy"
    if lower.startswith("registry/") or "/registry/" in lower:
        return "registry_state"
    if lower.startswith("tests/") or "/tests/" in lower or name.startswith("test_"):
        return "test_or_fixture"
    if lower.startswith("data/") or "/data/" in lower:
        return "data"
    if lower.startswith("reports/") or "/reports/" in lower or "qa_report" in name or "audit_report" in name:
        return "report_or_evidence"
    if lower.startswith("releases/") or "/releases/" in lower or name.startswith(("install_", "rollback_", "commit_message_")):
        return "release_control"
    if suffix in SCHEMA_SUFFIXES:
        return "structured_configuration"
    guessed, _ = mimetypes.guess_type(name)
    if guessed and guessed.startswith("image/"):
        return "image_asset"
    if guessed and guessed.startswith("audio/"):
        return "audio_asset"
    return "other_artifact"


def classify_lifecycle(rel_path: str) -> str:
    lower = rel_path.lower()
    name = Path(rel_path).name.lower()
    if any(token in lower for token in ("/archive/", "archive/", "historical", "deprecated", "superseded", "root_archive")):
        return "historical_or_archived"
    if any(token in lower for token in ("/generated/", "generated/", "/build/", "/dist/")):
        return "generated"
    if any(token in name for token in ("patch_manifest", "file_hashes", "file_index", "artifact_inventory", "qa_report")):
        return "release_evidence"
    if any(token in lower for token in ("/fixtures/", "/fixture/", "/tests/", "tests/")) or name.startswith("test_"):
        return "test_or_fixture"
    if any(token in lower for token in ("/patches/", "_patch/", "patches/")):
        return "migration_or_patch_artifact"
    return "active_or_unresolved"


def classify_authorship(rel_path: str) -> str:
    lower = rel_path.lower()
    name = Path(rel_path).name.lower()
    if any(token in lower for token in ("/generated/", "generated/", "/build/", "/dist/")):
        return "generated"
    if any(token in name for token in ("file_hashes", "file_index", "artifact_inventory", "patch_manifest", "qa_report")):
        return "generated_release_control"
    return "authored_or_legacy_authored"


def owner_domain(rel_path: str) -> str:
    lower = rel_path.lower()
    ordered = (
        (("unified_consolidation", "consolidation/uc01", "legacy_context_migration", "lcm_"), "consolidation_and_migration"),
        (("rthp",), "context_rthp"),
        (("saed", "context_intelligence", "edge_discovery"), "ai_research_and_edge_discovery"),
        (("ucee", "universal_context_exploitation"), "treatment_and_context_exploitation"),
        (("acl_os", "context_lifecycle"), "context_lifecycle_governance"),
        (("strategy_factory",), "strategy_factory"),
        (("nds", "hook_864", "hook_validity"), "nds_and_hook_systems"),
        (("exp0017",), "experiment_exp0017"),
        (("exp0018",), "experiment_exp0018"),
        (("exp0019", "faerie"), "experiment_exp0019"),
        (("mql5",), "mql5_runtime_and_visualization"),
        (("engineering", "github", "agents.md"), "engineering_governance"),
        (("product_lab", "products/"), "product_lab"),
        (("docs/",), "documentation_and_knowledge"),
        (("registry/",), "registry_and_control_plane"),
        (("research/",), "research_workbench"),
        (("data/",), "data_assets"),
        (("tests/",), "test_infrastructure"),
        (("tools/",), "developer_tooling"),
        (("lab/",), "legacy_lab_topology"),
    )
    for tokens, domain in ordered:
        if any(token in lower for token in tokens):
            return domain
    top = rel_path.split("/", 1)[0].lower()
    return f"repository_{top or 'root'}"


def critical_domains(rel_path: str, symbol_text: str = "") -> list[str]:
    haystack = f"{rel_path} {symbol_text}".lower()
    found = [domain for domain, patterns in CRITICAL_DOMAIN_PATTERNS.items() if any(pattern in haystack for pattern in patterns)]
    return sorted(set(found))


def criticality(rel_path: str, category: str) -> str:
    domains = critical_domains(rel_path)
    lower = rel_path.lower()
    if category == "source_code" and domains:
        if any(token in lower for token in ("execution", "order", "broker", "capital", "authority", "known_time", "runtime")):
            return "critical"
        return "high"
    if category in {"schema", "policy", "registry_state"} and domains:
        return "high"
    if category in {"source_code", "schema", "policy"}:
        return "medium"
    return "normal"


def probable_production_source(rel_path: str) -> bool:
    lower = rel_path.lower()
    if Path(rel_path).suffix.lower() not in SOURCE_SUFFIXES:
        return False
    excluded = (
        "/tests/", "tests/", "/fixtures/", "/examples/", "examples/", "/archive/", "archive/",
        "/patches/", "_patch/", "/generated/", "generated/", "/releases/", "releases/",
    )
    return not any(token in lower for token in excluded)
