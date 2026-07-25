"""Deterministic authority, destination and disposition classification."""
from __future__ import annotations

import re
from pathlib import PurePosixPath

ROOT_RELEASE_RE = re.compile(
    r"^(?:README_|INSTALL_|ROLLBACK_|COMMIT_MESSAGE_|.*_FILE_INDEX|.*_FILE_HASHES|"
    r".*_PATCH_MANIFEST|.*_QA_REPORT|.*_ARTIFACT_INVENTORY|.*_PATCH_CONTENTS_TREE|"
    r".*_TAG_MESSAGE)",
    re.IGNORECASE,
)

DOMAIN_TARGETS = {
    "kernel": "src/engine/kernel",
    "market": "src/engine/market",
    "context": "src/engine/context",
    "treatment": "src/engine/treatment",
    "research": "src/engine/research",
    "evidence": "src/engine/evidence",
    "policy": "src/engine/policy",
    "capital": "src/engine/capital",
    "portfolio": "src/engine/portfolio",
    "runtime": "src/engine/runtime",
    "execution": "src/engine/execution",
    "monitoring": "src/engine/monitoring",
    "memory": "src/engine/memory",
    "adapters": "adapters",
    "contracts": "contracts",
    "schemas": "schemas",
    "registry": "registry",
    "configuration": "configs",
    "mql5": "mql5",
    "testing": "tests",
    "documentation": "docs",
    "engineering": "tools",
    "operations": "ops",
    "products": "products",
    "examples": "examples",
    "release_history": "releases/history",
    "historical_archive": "releases/archive",
}


def _contains(path: str, *tokens: str) -> bool:
    lowered = path.lower()
    return any(token in lowered for token in tokens)


def _strategy_factory_domain(path: str) -> str:
    lowered = path.lower()
    if "rthp" in lowered:
        return "context"
    if _contains(lowered, "market", "session", "calendar", "symbol", "data_sync", "time_kernel"):
        return "market"
    if _contains(lowered, "context", "occurrence", "detector", "confirmation", "invalidation"):
        return "context"
    if _contains(lowered, "treatment", "setup", "entry", "stop", "target", "management", "abstain"):
        return "treatment"
    if _contains(lowered, "evidence", "promotion", "qualification", "falsification", "final_test", "reproduc"):
        return "evidence"
    if _contains(lowered, "portfolio", "allocation"):
        return "portfolio"
    if _contains(lowered, "capital", "economics", "risk", "sizing"):
        return "capital"
    if _contains(lowered, "runtime", "live", "deployment", "lease", "rollback", "recovery"):
        return "runtime"
    if _contains(lowered, "execution", "broker", "order", "position", "fill", "slippage"):
        return "execution"
    if _contains(lowered, "monitor", "surveillance", "incident", "drift", "health", "retirement"):
        return "monitoring"
    if _contains(lowered, "policy", "governance"):
        return "policy"
    if _contains(lowered, "contract", "validation", "identity", "lineage", "registry", "anatomy"):
        return "kernel"
    if _contains(
        lowered,
        "research", "feature", "label", "dataset", "train", "model", "experiment",
        "statistics", "tournament", "outcome", "candidate", "inference", "advanced_task",
        "classical", "deep_view",
    ):
        return "research"
    if _contains(lowered, "plugin", "integration", "onboarding", "generation"):
        return "adapters"
    return "research"


def _saed_domain(path: str) -> str:
    lowered = path.lower()
    if _contains(lowered, "runtime", "micro_live", "immutable_runtime"):
        return "runtime"
    if _contains(lowered, "portfolio", "execution_economics"):
        return "portfolio"
    if _contains(lowered, "treatment", "action_lattice", "setup_reasoning"):
        return "treatment"
    if _contains(lowered, "surveillance", "retirement"):
        return "monitoring"
    if _contains(lowered, "research_memory", "active_planner"):
        return "memory"
    if _contains(lowered, "constitution", "formal_verification", "model_risk", "supply_chain"):
        return "policy"
    return "research"


def _system_id(path: str) -> str:
    lowered = path.lower()
    if "strategy_factory_rthp" in lowered or "/contexts/rthp" in lowered or "rthp_" in PurePosixPath(path).name.lower():
        return "RTHP"
    if "saed_v4" in lowered:
        return "SAED_V4"
    if "saed_v3" in lowered:
        return "SAED_V3"
    if "ucee" in lowered or "universal_context_engine" in lowered:
        return "UCEE"
    if "acl_os" in lowered or "context_lifecycle_os" in lowered or "acl_" in PurePosixPath(path).name.lower():
        return "ACL_OS"
    if "/lcm/" in lowered or "legacy_context_migration" in lowered or PurePosixPath(path).name.lower().startswith("lcm_"):
        return "LCM"
    if "ai_algorithm_engineering_os" in lowered or "aieos" in lowered:
        return "AIEOS"
    if "nds" in lowered:
        return "NDS"
    if "exp001" in lowered or "/experiments/" in lowered:
        return "EXPERIMENTS"
    if "strategy_factory" in lowered:
        return "STRATEGY_FACTORY"
    return "CORE_OR_OTHER"


def classify_artifact(row: dict) -> dict:
    path = str(row["path"]).replace("\\", "/")
    lowered = path.lower()
    parts = PurePosixPath(path).parts
    root = parts[0] if parts else path
    category = row.get("category")
    production = bool(row.get("production_source_candidate"))
    system_id = _system_id(path)

    domain: str
    disposition: str
    target: str
    wave: str
    action: str
    rationale: str
    confidence = "HIGH"

    # Repository-level canonical files.
    if "/" not in path and path in {
        "README.md", "AGENTS.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md", "LICENSE",
        "pyproject.toml", "uv.lock", ".gitignore", ".gitattributes", ".editorconfig",
    }:
        domain, disposition, target, wave, action = "engineering", "KEEP_CANONICAL", path, "UC03-W01-ROOT", "KEEP"
        rationale = "Canonical repository control or project entry document."
    elif "/" not in path and ROOT_RELEASE_RE.match(path):
        domain, disposition, target, wave, action = "release_history", "EXTERNALIZE", "releases/history/root-bundles", "UC03-W01-ROOT", "MOVE_TO_HISTORY"
        rationale = "Root-level phase or release artifact is grandfathered history and must leave the final root."
    elif root == ".github":
        domain, disposition, target, wave, action = "engineering", "KEEP_CANONICAL", path, "UC03-W01-ROOT", "KEEP_OR_NORMALIZE"
        rationale = "Repository automation and contribution governance."
    elif root == ".obsidian":
        domain, disposition, target, wave, action = "documentation", "KEEP_CANONICAL", path, "UC03-W04-DOCS", "KEEP_OR_NORMALIZE"
        rationale = "Obsidian workspace configuration."
    elif root == "docs":
        domain, disposition, target, wave, action = "documentation", "MERGE", "docs", "UC03-W04-DOCS", "CLASSIFY_AND_COLLAPSE"
        rationale = "Documentation must converge to one authority tree while preserving normative meaning and history."
    elif root == "mql5":
        domain, disposition, target, wave, action = "mql5", "MOVE", "mql5", "UC03-W05-MQL5", "NORMALIZE_MQL5_TOPOLOGY"
        rationale = "MQL5 source is retained and normalized under the canonical terminal boundary."
    elif root == "tests":
        domain, disposition, target, wave, action = "testing", "MOVE", "tests", "UC03-W06-TESTS", "UNIFY_TEST_TOPOLOGY"
        rationale = "Verification assets converge into one test root."
    elif root == "registry":
        domain, disposition, target, wave, action = "registry", "MERGE", "registry", "UC03-W07-REGISTRY", "NORMALIZE_REGISTRY_AUTHORITY"
        rationale = "Identity, lineage and state records remain under the registry authority boundary."
    elif root == "schemas":
        domain, disposition, target, wave, action = "schemas", "KEEP_CANONICAL", "schemas", "UC03-W03-CONTRACTS", "KEEP_OR_NORMALIZE"
        rationale = "Schema authority belongs under the canonical schema root."
    elif root == "policies":
        domain, disposition, target, wave, action = "policy", "KEEP_CANONICAL", "policies", "UC03-W03-CONTRACTS", "KEEP_OR_NORMALIZE"
        rationale = "Machine-governance policies belong under the canonical policy root."
    elif root == "contracts":
        domain, disposition, target, wave, action = "contracts", "KEEP_CANONICAL", "contracts", "UC03-W03-CONTRACTS", "KEEP_OR_NORMALIZE"
        rationale = "Normative interfaces belong under the canonical contract root."
    elif root == "configs":
        domain, disposition, target, wave, action = "configuration", "KEEP_CANONICAL", "configs", "UC03-W03-CONTRACTS", "KEEP_OR_NORMALIZE"
        rationale = "Non-secret configuration belongs under the canonical configuration root."
    elif root == "releases":
        domain, disposition, target, wave, action = "release_history", "MERGE", "releases", "UC03-W08-RELEASES", "NORMALIZE_RELEASE_HISTORY"
        rationale = "Release controls remain indexed but phase sprawl is collapsed."
    elif root in {"product_lab", "products"}:
        domain, disposition, target, wave, action = "products", "MOVE", "products", "UC03-W09-PRODUCTS", "NORMALIZE_PRODUCT_SURFACES"
        rationale = "Product-facing assets converge under the products root."
    elif root == "examples":
        domain, disposition, target, wave, action = "examples", "KEEP_CANONICAL", "examples", "UC03-W09-PRODUCTS", "KEEP_OR_NORMALIZE"
        rationale = "Bounded examples remain outside the production engine."
    elif root in {"data", "reports"}:
        domain, disposition, target, wave, action = "historical_archive", "EXTERNALIZE", ".alpha/artifacts", "UC03-W10-GENERATED", "EXTERNALIZE_RUNTIME_OUTPUT"
        rationale = "Data and report outputs must not remain mixed with authored source."
    elif root == "research" and not production:
        domain, disposition, target, wave, action = "historical_archive", "EXTERNALIZE", "releases/archive/research", "UC03-W10-GENERATED", "CLASSIFY_RESEARCH_ARTIFACT"
        rationale = "Research outputs are preserved externally unless explicitly promoted to authored source."
    elif root == "papers":
        domain, disposition, target, wave, action = "documentation", "MOVE", "docs/references", "UC03-W04-DOCS", "MOVE_REFERENCE_MATERIAL"
        rationale = "Research papers are reference documentation, not production code."
    elif root == "ops":
        domain, disposition, target, wave, action = "operations", "KEEP_CANONICAL", "ops", "UC03-W11-OPS", "KEEP_OR_NORMALIZE"
        rationale = "Operational automation belongs under the operations root."
    elif root == "adapters":
        domain, disposition, target, wave, action = "adapters", "KEEP_CANONICAL", "adapters", "UC03-W03-CONTRACTS", "KEEP_OR_NORMALIZE"
        rationale = "External integration boundaries remain adapters."
    elif root == "contexts":
        domain, disposition, target, wave, action = "context", "KEEP_CANONICAL", "contexts", "UC03-W02-CODE", "KEEP_OR_NORMALIZE"
        rationale = "Authored Context packages belong under the canonical Context root."
    elif root == "src":
        domain = _strategy_factory_domain(path)
        disposition, target, wave, action = "MERGE", DOMAIN_TARGETS[domain], "UC03-W02-CODE", "NORMALIZE_PRODUCTION_ROOT"
        rationale = "Production source converges under src/engine with one authority per capability."
    elif root == "tools":
        if lowered.startswith("tools/consolidation/") or lowered.startswith("tools/engineering/"):
            domain, disposition, target, wave, action = "engineering", "KEEP_CANONICAL", "tools", "UC03-W11-OPS", "KEEP_MAINTENANCE_TOOL"
            rationale = "Developer, verification and migration tooling remains under tools."
        elif "/lcm/" in lowered:
            domain, disposition, target, wave, action = "engineering", "MERGE", "tools/maintenance", "UC03-W11-OPS", "RETAIN_REUSABLE_MAINTENANCE_ONLY"
            rationale = "Reusable LCM verification and recovery logic survives; phase machinery becomes history."
        elif "rthp" in lowered:
            domain, disposition, target, wave, action = "context", "MERGE", "contexts/rthp", "UC03-W02-CODE", "SPLIT_SHARED_AND_CONTEXT"
            rationale = "RTHP-specific tooling becomes a Context package; shared mechanisms move into the engine."
        elif "saed" in lowered:
            domain, disposition, target, wave, action = _saed_domain(path), "MERGE", "src/engine/extensions/saed", "UC03-W02-CODE", "CONVERT_TO_EXTENSION"
            rationale = "SAED becomes a bounded research extension and loses parallel platform authority."
        elif "strategy_factory" in lowered or "acl_os" in lowered or "ucee" in lowered:
            domain = _strategy_factory_domain(path)
            disposition, target, wave, action = "MERGE", DOMAIN_TARGETS[domain], "UC03-W02-CODE", "PORT_SHARED_LOGIC_THEN_RETIRE_TOOL_ENGINE"
            rationale = "Shared engine logic cannot remain under tools; only developer utilities stay there."
        else:
            domain, disposition, target, wave, action = "engineering", "KEEP_CANONICAL", "tools", "UC03-W11-OPS", "REVIEW_AS_DEVELOPER_TOOL"
            rationale = "Non-engine tooling remains under the developer utility boundary."
    elif root == "lab":
        if "saed_v4" in lowered or "saed_v3" in lowered:
            domain = _saed_domain(path)
            disposition, target, wave, action = "MERGE", "src/engine/extensions/saed", "UC03-W02-CODE", "CONVERT_TO_EXTENSION"
            rationale = "SAED logic is retained as an extension, not as a parallel platform."
        elif "rthp" in lowered:
            domain, disposition, target, wave, action = "context", "MERGE", "contexts/rthp", "UC03-W02-CODE", "SPLIT_SHARED_AND_CONTEXT"
            rationale = "RTHP-specific semantics move to contexts/rthp while shared code moves to src/engine."
        elif "strategy_factory" in lowered or "ucee" in lowered or "acl" in lowered:
            domain = _strategy_factory_domain(path)
            disposition, target, wave, action = "MERGE", DOMAIN_TARGETS[domain], "UC03-W02-CODE", "PORT_BEHAVIOR_AND_RETIRE_PARALLEL_ENGINE"
            rationale = "Legacy production logic must be preserved and merged into the single engine authority."
        elif production:
            domain = _strategy_factory_domain(path)
            disposition, target, wave, action = "MOVE", DOMAIN_TARGETS[domain], "UC03-W02-CODE", "MOVE_PRODUCTION_SOURCE"
            rationale = "Production source may not remain under lab."
        else:
            domain, disposition, target, wave, action = "historical_archive", "EXTERNALIZE", "releases/archive/lab", "UC03-W10-GENERATED", "ARCHIVE_NON_PRODUCTION_LAB_ASSET"
            rationale = "Non-production laboratory material is preserved outside the final working tree."
    elif category == "documentation":
        domain, disposition, target, wave, action = "documentation", "MOVE", "docs", "UC03-W04-DOCS", "CLASSIFY_DOCUMENT"
        rationale = "Documentation outside the canonical tree must be normalized."
    elif production:
        domain = _strategy_factory_domain(path)
        disposition, target, wave, action = "MOVE", DOMAIN_TARGETS[domain], "UC03-W02-CODE", "MOVE_PRODUCTION_SOURCE"
        rationale = "Unconventional production source receives a canonical domain and destination."
        confidence = "MEDIUM"
    else:
        domain, disposition, target, wave, action = "historical_archive", "EXTERNALIZE", "releases/archive/misc", "UC03-W10-GENERATED", "PRESERVE_AND_CLASSIFY_HISTORY"
        rationale = "Residual non-production artifact is preserved as history rather than left unowned."
        confidence = "MEDIUM"

    return {
        "path": path,
        "source_sha256": row.get("sha256"),
        "source_category": category,
        "source_owner_domain": row.get("owner_domain"),
        "production_source_candidate": production,
        "system_id": system_id,
        "canonical_owner": domain,
        "canonical_target": target,
        "planning_disposition": disposition,
        "migration_action": action,
        "migration_wave": wave,
        "classification_confidence": confidence,
        "review_required": confidence != "HIGH",
        "rationale": rationale,
        "destructive_authority": False,
        "runtime_authority": False,
        "order_authority": False,
        "broker_authority": False,
        "capital_authority": False,
    }


def classify_symbol(path: str, name: str, kind: str, language: str) -> dict:
    artifact = classify_artifact({
        "path": path,
        "sha256": None,
        "category": "source_code",
        "owner_domain": None,
        "production_source_candidate": True,
    })
    return {
        "language": language,
        "path": path,
        "symbol": name,
        "symbol_kind": kind,
        "system_id": artifact["system_id"],
        "canonical_owner": artifact["canonical_owner"],
        "canonical_target": artifact["canonical_target"],
        "migration_action": artifact["migration_action"],
        "destructive_authority": False,
    }
