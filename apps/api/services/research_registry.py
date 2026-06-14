from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable, Literal

from apps.api.core.config import settings

DOC_EXTENSIONS = {".md", ".yaml", ".yml", ".txt", ".py", ".json"}
TEXT_DOC_EXTENSIONS = {".md", ".yaml", ".yml", ".txt", ".py", ".json"}

StageId = Literal[
    "observations",
    "hypotheses",
    "metrics",
    "experiments",
    "analysis",
    "validation",
    "production",
    "monitoring",
    "archive",
    "execution",
    "infrastructure",
    "core",
    "docs",
    "registry",
    "unknown",
]

STAGES: list[dict[str, str]] = [
    {"stage_id": "observations", "label": "Observations", "folder": "lab/01_observation", "description": "Raw market observations and recurring behaviors."},
    {"stage_id": "hypotheses", "label": "Hypotheses", "folder": "lab/02_hypotheses", "description": "Falsifiable market claims derived from observations."},
    {"stage_id": "metrics", "label": "Metrics", "folder": "lab/core", "description": "Metric specifications and code modules."},
    {"stage_id": "experiments", "label": "Experiments", "folder": "lab/03_experiments", "description": "Runnable tests, experiment plans, and experiment reports."},
    {"stage_id": "analysis", "label": "Analysis", "folder": "lab/04_analysis", "description": "Post-experiment interpretation and analysis notes."},
    {"stage_id": "validation", "label": "Validation", "folder": "lab/05_validation", "description": "Leakage, baseline, walk-forward, robustness, and OOS checks."},
    {"stage_id": "production", "label": "Production", "folder": "lab/06_production", "description": "Signal definitions promoted toward production."},
    {"stage_id": "monitoring", "label": "Monitoring", "folder": "lab/07_monitoring", "description": "Live health, drift, degradation, and monitoring records."},
    {"stage_id": "archive", "label": "Archive", "folder": "lab/08_archive", "description": "Rejected ideas, failed experiments, and retired signals."},
    {"stage_id": "execution", "label": "Execution", "folder": "lab/09_execution", "description": "Execution bridge, logging, and execution design notes."},
    {"stage_id": "infrastructure", "label": "Infrastructure", "folder": "lab/10_infrastructure", "description": "CI, configuration, data, and operational docs."},
    {"stage_id": "core", "label": "Core Engines", "folder": "lab/core", "description": "Market data, structural nodes, detectors, and reusable engines."},
    {"stage_id": "docs", "label": "Project Docs", "folder": "docs", "description": "Manifesto, principles, architecture, glossary, roadmap, UI contracts."},
    {"stage_id": "registry", "label": "Registries", "folder": "registry", "description": "YAML and machine-readable project registries."},
]

ID_RE = re.compile(r"\b(OBS\d+|H\d+|M\d+|EXP\d+|ANL\d+|VAL\d+|SIG\d+|MON\d+|CP\d+|RUN\d+)\b", re.IGNORECASE)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)
STATUS_RE = re.compile(r"^\s*(?:##\s*)?Status\s*[:\-]?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
VERSION_RE = re.compile(r"^\s*(?:##\s*)?Version\s*[:\-]?\s*(.+)$", re.IGNORECASE | re.MULTILINE)


@dataclass(frozen=True)
class LabDocument:
    doc_id: str
    title: str
    stage_id: str
    stage_label: str
    entity_type: str
    path: str
    extension: str
    status: str | None
    version: str | None
    summary: str
    relation_ids: list[str]
    tags: list[str]
    capabilities: list[str]
    size_bytes: int
    modified_time: float


@dataclass(frozen=True)
class ResearchEntity:
    id: str
    entity_type: str
    title: str
    stage_id: str
    stage_label: str
    status: str | None
    summary: str
    primary_path: str
    document_paths: list[str]
    relation_ids: list[str]
    tags: list[str]
    capabilities: list[str]


@dataclass(frozen=True)
class ResearchRun:
    run_id: str
    entity_id: str
    entity_type: str
    adapter_id: str
    symbol: str | None
    timeframe: str | None
    parameters: dict[str, object]
    artifact_path: str
    summary_stats: dict[str, object]
    validation_flags: list[dict[str, object]]
    created_time: float


def repo_root() -> Path:
    return settings.root_path.resolve()


def safe_relative_path(path: str) -> Path:
    root = repo_root()
    candidate = (root / path).resolve()
    if candidate != root and root not in candidate.parents:
        raise ValueError("Path escapes repository root")
    return candidate


def stage_for_path(path: Path) -> dict[str, str]:
    rel = path.relative_to(repo_root()).as_posix()
    best: dict[str, str] | None = None
    best_len = -1
    for stage in STAGES:
        folder = stage["folder"].rstrip("/")
        if rel == folder or rel.startswith(folder + "/"):
            if len(folder) > best_len:
                best = stage
                best_len = len(folder)
    return best or {"stage_id": "unknown", "label": "Unknown", "folder": "", "description": ""}


def list_documents(stage_id: str | None = None, query: str | None = None) -> list[LabDocument]:
    root = repo_root()
    docs: list[LabDocument] = []
    folders = {stage["folder"]: stage for stage in STAGES}

    for stage in STAGES:
        if stage_id and stage_id not in {"all", stage["stage_id"]}:
            continue
        folder = root / stage["folder"]
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if should_skip_path(path):
                continue
            if path.is_file() and path.suffix.lower() in DOC_EXTENSIONS:
                try:
                    doc = build_document(path, stage_for_path(path))
                except OSError:
                    continue
                docs.append(doc)

    # Make sure metric specs under core/metrics are not hidden by stage filtering.
    if stage_id in {None, "all", "metrics"}:
        for path in sorted((root / "lab").rglob("M*.md")):
            if path.is_file() and not should_skip_path(path):
                try:
                    doc = build_document(path, stage_for_path(path))
                except OSError:
                    continue
                if doc.doc_id.startswith("M") and doc.path not in {d.path for d in docs}:
                    docs.append(doc)

    if query:
        needle = query.lower().strip()
        docs = [
            doc for doc in docs
            if needle in f"{doc.doc_id} {doc.title} {doc.path} {doc.summary} {doc.status or ''} {' '.join(doc.tags)}".lower()
        ]

    docs = sorted(unique_docs(docs), key=lambda doc: (stage_sort_key(doc.stage_id), doc.doc_id, doc.path))
    return docs


def unique_docs(docs: Iterable[LabDocument]) -> list[LabDocument]:
    seen: set[str] = set()
    out: list[LabDocument] = []
    for doc in docs:
        if doc.path in seen:
            continue
        seen.add(doc.path)
        out.append(doc)
    return out


def list_stages() -> list[dict[str, object]]:
    docs = list_documents()
    counts: dict[str, int] = {}
    for doc in docs:
        counts[doc.stage_id] = counts.get(doc.stage_id, 0) + 1
    return [{**stage, "count": counts.get(stage["stage_id"], 0)} for stage in STAGES]


def read_document(path: str) -> dict[str, object]:
    candidate = safe_relative_path(path)
    if not candidate.exists() or not candidate.is_file():
        raise FileNotFoundError(path)
    if candidate.suffix.lower() not in TEXT_DOC_EXTENSIONS:
        raise ValueError("Unsupported document type")
    content = candidate.read_text(encoding="utf-8", errors="replace")
    doc = build_document(candidate, stage_for_path(candidate))
    return {
        "doc": asdict(doc),
        "content": content,
        "outline": extract_outline(content),
        "front_matter": extract_front_matter(content),
        "relations": related_entities_for_doc(doc),
    }


def list_entities(entity_type: str | None = None, query: str | None = None) -> list[ResearchEntity]:
    docs = list_documents(query=query)
    grouped: dict[str, list[LabDocument]] = {}
    for doc in docs:
        grouped.setdefault(doc.doc_id, []).append(doc)

    entities: list[ResearchEntity] = []
    for entity_id, entity_docs in grouped.items():
        primary = choose_primary_document(entity_docs)
        etype = infer_entity_type(primary.doc_id, primary.path, primary.stage_id)
        if entity_type and entity_type != "all" and etype != entity_type:
            continue
        relation_ids = sorted({rel for doc in entity_docs for rel in doc.relation_ids if rel != entity_id})
        tags = sorted({tag for doc in entity_docs for tag in doc.tags})
        capabilities = sorted({cap for doc in entity_docs for cap in doc.capabilities})
        entities.append(ResearchEntity(
            id=entity_id,
            entity_type=etype,
            title=primary.title,
            stage_id=primary.stage_id,
            stage_label=primary.stage_label,
            status=primary.status,
            summary=primary.summary,
            primary_path=primary.path,
            document_paths=[doc.path for doc in entity_docs],
            relation_ids=relation_ids,
            tags=tags,
            capabilities=capabilities,
        ))

    return sorted(entities, key=lambda e: (entity_sort_key(e.entity_type), e.id))


def get_entity(entity_id: str) -> ResearchEntity | None:
    entity_id = entity_id.upper()
    for entity in list_entities():
        if entity.id.upper() == entity_id:
            return entity
    return None


def overview() -> dict[str, object]:
    docs = list_documents()
    entities = list_entities()
    runs = list_runs()

    stats = {
        "documents": len(docs),
        "entities": len(entities),
        "observations": count_entities(entities, "observation"),
        "hypotheses": count_entities(entities, "hypothesis"),
        "metrics": count_entities(entities, "metric"),
        "experiments": count_entities(entities, "experiment"),
        "validations": count_entities(entities, "validation"),
        "runs": len(runs),
    }

    critical_path = [
        {"id": "OBS0001", "label": "Structural highs/lows", "stage": "Observation"},
        {"id": "H0001", "label": "Decision nodes", "stage": "Hypothesis"},
        {"id": "H0002", "label": "Node territories", "stage": "Hypothesis"},
        {"id": "M0001", "label": "Relative Territory Volatility", "stage": "Metric"},
        {"id": "EXP0001", "label": "Real-market inspection", "stage": "Experiment"},
        {"id": "VAL0001", "label": "Validation gates", "stage": "Validation"},
    ]

    return {
        "stats": stats,
        "stages": list_stages(),
        "entities": [asdict(entity) for entity in entities[:200]],
        "lineage": build_graph(entities),
        "critical_path": critical_path,
        "recent_runs": [asdict(run) for run in runs[:20]],
        "health": lab_health(entities, runs),
    }


def build_graph(entities: list[ResearchEntity] | None = None) -> dict[str, object]:
    entities = entities or list_entities()
    entity_ids = {e.id for e in entities}
    nodes = [
        {
            "id": entity.id,
            "type": entity.entity_type,
            "label": entity.title,
            "stage_id": entity.stage_id,
            "status": entity.status,
            "path": entity.primary_path,
            "capabilities": entity.capabilities,
        }
        for entity in entities
    ]
    edges = []
    for entity in entities:
        for rel in entity.relation_ids:
            if rel in entity_ids:
                edges.append({"source": entity.id, "target": rel, "kind": "references"})
    return {"nodes": nodes, "edges": edges}


def list_runs(entity_id: str | None = None) -> list[ResearchRun]:
    runs: list[ResearchRun] = []
    runs.extend(discover_m0001_runs())
    if entity_id and entity_id != "all":
        entity_id = entity_id.upper()
        runs = [run for run in runs if run.entity_id == entity_id]
    return sorted(runs, key=lambda run: run.created_time, reverse=True)


def discover_m0001_runs() -> list[ResearchRun]:
    root = repo_root()
    paths = []
    metric_root = root / "lab/cache_metrics/M0001_relative_territory_volatility"
    if metric_root.exists():
        paths.extend(metric_root.rglob("*.parquet"))

    out: list[ResearchRun] = []
    for path in paths:
        rel = path.relative_to(root).as_posix()
        symbol, timeframe, params = parse_m0001_path(path)
        stats = read_metric_stats(path)
        digest = hashlib.sha1(rel.encode("utf-8")).hexdigest()[:10].upper()
        flags = metric_validation_flags(stats)
        out.append(ResearchRun(
            run_id=f"RUN-M0001-{digest}",
            entity_id="M0001",
            entity_type="metric_run",
            adapter_id="M0001_RTV",
            symbol=symbol,
            timeframe=timeframe,
            parameters=params,
            artifact_path=rel,
            summary_stats=stats,
            validation_flags=flags,
            created_time=path.stat().st_mtime,
        ))
    return out


def parse_m0001_path(path: Path) -> tuple[str | None, str | None, dict[str, object]]:
    parts = path.parts
    symbol = None
    timeframe = None
    params: dict[str, object] = {}

    # Supports both:
    # lab/cache_metrics/M0001/.../GOLD/M15/GOLD_M15_T0.9_G6_hunt.parquet
    # lab/cache_metrics/M0001/.../L_5/GOLD/M15/GOLD_M15_L5_ZR0.9_EG6_hunt.parquet
    name = path.stem
    m = re.search(r"(?P<symbol>.+)_(?P<tf>M\d+|H\d+|D1|W1|MN1)", name)
    if m:
        symbol = m.group("symbol")
        timeframe = m.group("tf")

    if "L_" in parts:
        for part in parts:
            if re.fullmatch(r"L_\d+", part):
                params["L"] = int(part.split("_")[1])

    l = re.search(r"(?:_L|L_?)(\d+)", name)
    if l:
        params["L"] = int(l.group(1))

    zr = re.search(r"(?:ZR|T)([0-9.]+)", name)
    if zr:
        try:
            params["zone_ratio"] = float(zr.group(1).rstrip("."))
        except ValueError:
            pass
    eg = re.search(r"(?:EG|G)(\d+)", name)
    if eg:
        params["exit_gap"] = int(eg.group(1))
    if name.endswith("_hunt") or "_hunt" in name:
        params["consumption_mode"] = "hunt"
    if name.endswith("_touch") or "_touch" in name:
        params["consumption_mode"] = "touch"
    return symbol, timeframe, params


def read_metric_stats(path: Path) -> dict[str, object]:
    try:
        import pandas as pd
        df = pd.read_parquet(path)
    except Exception:
        return {"rows": None, "read_error": True}

    stats: dict[str, object] = {"rows": int(len(df))}
    rtv_col = "RTV" if "RTV" in df.columns else None
    if rtv_col:
        stats["mean_RTV"] = safe_float(df[rtv_col].mean())
        stats["median_RTV"] = safe_float(df[rtv_col].median())
    if "revisit_id" in df.columns and len(df):
        stats["max_revisit"] = int(df["revisit_id"].max())
    if "hunted" in df.columns and len(df):
        stats["hunted_events"] = int(df["hunted"].fillna(False).astype(bool).sum())
    return stats


def metric_validation_flags(stats: dict[str, object]) -> list[dict[str, object]]:
    rows = stats.get("rows")
    flags = [
        {"id": "schema_readable", "label": "Metric artifact readable", "status": "pass" if not stats.get("read_error") else "fail"},
        {"id": "events_present", "label": "Events present", "status": "pass" if isinstance(rows, int) and rows > 0 else "warn"},
    ]
    if "mean_RTV" in stats:
        flags.append({"id": "rtv_numeric", "label": "RTV numeric", "status": "pass"})
    return flags


def build_document(path: Path, stage: dict[str, str]) -> LabDocument:
    rel = path.relative_to(repo_root()).as_posix()
    content = read_preview(path)
    doc_id = extract_doc_id(path.name, content)
    title = extract_title(content) or title_from_path(path)
    entity_type = infer_entity_type(doc_id, rel, stage["stage_id"])
    status = extract_match(STATUS_RE, content)
    version = extract_match(VERSION_RE, content)
    summary = extract_summary(content)
    relation_ids = sorted({match.upper() for match in ID_RE.findall(content) if match.upper() != doc_id})[:32]
    tags = infer_tags(path, content, doc_id, stage["stage_id"])
    capabilities = infer_capabilities(path, content, doc_id)
    stat = path.stat()
    return LabDocument(
        doc_id=doc_id,
        title=title,
        stage_id=normalize_stage(stage["stage_id"], doc_id, rel),
        stage_label=stage_label(normalize_stage(stage["stage_id"], doc_id, rel)),
        entity_type=entity_type,
        path=rel,
        extension=path.suffix.lower().lstrip("."),
        status=status,
        version=version,
        summary=summary,
        relation_ids=relation_ids,
        tags=tags,
        capabilities=capabilities,
        size_bytes=stat.st_size,
        modified_time=stat.st_mtime,
    )


def normalize_stage(stage_id: str, doc_id: str, path: str) -> str:
    if doc_id.startswith("M"):
        return "metrics"
    if doc_id.startswith("EXP"):
        return "experiments"
    if doc_id.startswith("VAL"):
        return "validation"
    return stage_id


def stage_label(stage_id: str) -> str:
    for stage in STAGES:
        if stage["stage_id"] == stage_id:
            return stage["label"]
    return stage_id.title()


def infer_entity_type(doc_id: str, path: str, stage_id: str) -> str:
    if doc_id.startswith("OBS"):
        return "observation"
    if doc_id.startswith("H"):
        return "hypothesis"
    if doc_id.startswith("M"):
        return "metric"
    if doc_id.startswith("EXP"):
        return "experiment"
    if doc_id.startswith("VAL"):
        return "validation"
    if doc_id.startswith("SIG"):
        return "signal"
    if doc_id.startswith("MON"):
        return "monitoring"
    if doc_id.startswith("CP"):
        return "core"
    if stage_id == "hypotheses":
        return "hypothesis"
    if stage_id == "experiments":
        return "experiment"
    if stage_id == "validation":
        return "validation"
    return "document"


def infer_tags(path: Path, content: str, doc_id: str, stage_id: str) -> list[str]:
    tags = {stage_id, infer_entity_type(doc_id, path.as_posix(), stage_id)}
    lower = f"{path.as_posix()} {content[:4000]}".lower()
    for keyword in ["rtv", "volatility", "territory", "node", "revisit", "baseline", "walk-forward", "execution", "mt5", "validation", "leakage"]:
        if keyword in lower:
            tags.add(keyword)
    return sorted(tags)


def infer_capabilities(path: Path, content: str, doc_id: str) -> list[str]:
    caps = ["read"]
    lower = f"{path.as_posix()} {content[:3000]}".lower()
    if doc_id.startswith("M"):
        caps.extend(["visualize", "run", "compare_runs", "inspect_schema"])
    if "m0001" in lower or doc_id == "M0001":
        caps.extend(["chart_replay", "overlay_events", "overlay_nodes", "rtv_table"])
    if doc_id.startswith("H"):
        caps.extend(["test_on_chart", "link_experiment"])
    if doc_id.startswith("EXP"):
        caps.extend(["open_run", "visualize_artifacts"])
    return sorted(set(caps))


def choose_primary_document(docs: list[LabDocument]) -> LabDocument:
    def score(doc: LabDocument) -> tuple[int, int]:
        ext_score = 0 if doc.extension == "md" else 1
        spec_score = 0 if doc.doc_id in Path(doc.path).stem.upper() else 1
        return (ext_score + spec_score, len(doc.path))
    return sorted(docs, key=score)[0]


def read_preview(path: Path, max_chars: int = 16000) -> str:
    return path.read_text(encoding="utf-8", errors="replace")[:max_chars]


def extract_title(content: str) -> str | None:
    match = TITLE_RE.search(content)
    return match.group(1).strip() if match else None

def title_from_path(path: Path) -> str:
    name = path.stem.replace('_', ' ').replace('-', ' ').strip()
    return name.title() if name else path.name


def extract_doc_id(name: str, content: str) -> str:
    for source in (name, content[:1200]):
        match = ID_RE.search(source)
        if match:
            return match.group(1).upper()
    return Path(name).stem.upper().replace("-", "_")


def extract_match(pattern: re.Pattern[str], content: str) -> str | None:
    match = pattern.search(content)
    return match.group(1).strip().strip("*` ")[:120] if match else None


def extract_summary(content: str) -> str:
    lines = []
    in_fence = False
    for raw in content.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line:
            continue
        if line.startswith("#") or line.startswith("---") or re.match(r"^(version|status)\b", line, re.I):
            continue
        cleaned = re.sub(r"[*_`>#]", "", line).strip()
        if cleaned:
            lines.append(cleaned)
        if len(" ".join(lines)) > 240:
            break
    return " ".join(lines)[:360]


def extract_outline(content: str) -> list[dict[str, object]]:
    out = []
    for line_no, raw in enumerate(content.splitlines(), start=1):
        match = re.match(r"^(#{1,6})\s+(.+)$", raw)
        if match:
            out.append({"level": len(match.group(1)), "title": match.group(2).strip(), "line": line_no})
    return out[:120]


def extract_front_matter(content: str) -> dict[str, object]:
    if not content.startswith("---"):
        return {}
    end = content.find("\n---", 3)
    if end == -1:
        return {}
    result: dict[str, object] = {}
    for raw in content[3:end].splitlines():
        if ":" in raw:
            key, value = raw.split(":", 1)
            result[key.strip()] = value.strip()
    return result


def related_entities_for_doc(doc: LabDocument) -> list[dict[str, object]]:
    by_id = {entity.id: entity for entity in list_entities()}
    related = []
    for rel in doc.relation_ids:
        entity = by_id.get(rel)
        if entity:
            related.append(asdict(entity))
    return related


def docs_to_dicts(docs: Iterable[LabDocument]) -> list[dict[str, object]]:
    return [asdict(doc) for doc in docs]


def entities_to_dicts(entities: Iterable[ResearchEntity]) -> list[dict[str, object]]:
    return [asdict(entity) for entity in entities]


def runs_to_dicts(runs: Iterable[ResearchRun]) -> list[dict[str, object]]:
    return [asdict(run) for run in runs]


def lab_health(entities: list[ResearchEntity], runs: list[ResearchRun]) -> list[dict[str, object]]:
    ids = {entity.id for entity in entities}
    return [
        {"id": "registry", "label": "Research registry loaded", "status": "pass" if entities else "warn", "detail": f"{len(entities)} entities"},
        {"id": "m0001", "label": "M0001 discoverable", "status": "pass" if "M0001" in ids else "warn", "detail": "Metric spec/code entity"},
        {"id": "runs", "label": "Metric artifacts discovered", "status": "pass" if runs else "warn", "detail": f"{len(runs)} runs"},
        {"id": "lineage", "label": "Relations extracted", "status": "pass" if any(e.relation_ids for e in entities) else "warn", "detail": "Document ID links"},
    ]


def should_skip_path(path: Path) -> bool:
    parts = set(path.parts)
    return bool(parts & {".git", "__pycache__", "node_modules", "dist", ".vite", ".pytest_cache"})


def stage_sort_key(stage_id: str) -> int:
    order = [stage["stage_id"] for stage in STAGES]
    return order.index(stage_id) if stage_id in order else 999


def entity_sort_key(entity_type: str) -> int:
    order = ["observation", "hypothesis", "metric", "experiment", "analysis", "validation", "signal", "monitoring", "core", "document"]
    return order.index(entity_type) if entity_type in order else 999


def count_entities(entities: list[ResearchEntity], entity_type: str) -> int:
    return sum(1 for entity in entities if entity.entity_type == entity_type)


def safe_float(value) -> float | None:
    try:
        if value != value:
            return None
        return float(value)
    except Exception:
        return None
