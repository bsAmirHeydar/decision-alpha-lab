from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from apps.api.core.config import settings

DOC_EXTENSIONS = {".md", ".yaml", ".yml", ".py", ".txt"}

STAGES: list[dict[str, str]] = [
    {"stage_id": "observations", "label": "Observations", "folder": "lab/01_observation", "description": "Raw market observations and recurring behaviors."},
    {"stage_id": "hypotheses", "label": "Hypotheses", "folder": "lab/02_hypotheses", "description": "Formal falsifiable claims derived from observations."},
    {"stage_id": "experiments", "label": "Experiments", "folder": "lab/03_experiments", "description": "Runnable tests and experiment reports."},
    {"stage_id": "analysis", "label": "Analysis", "folder": "lab/04_analysis", "description": "Post-experiment notebooks, notes, and interpretation."},
    {"stage_id": "validation", "label": "Validation", "folder": "lab/05_validation", "description": "Out-of-sample, robustness, and leakage checks."},
    {"stage_id": "production", "label": "Production", "folder": "lab/06_production", "description": "Signal definitions promoted toward production."},
    {"stage_id": "monitoring", "label": "Monitoring", "folder": "lab/07_monitoring", "description": "Live health, drift, and degradation records."},
    {"stage_id": "archive", "label": "Archive", "folder": "lab/08_archive", "description": "Rejected ideas, failed experiments, and retired signals."},
    {"stage_id": "execution", "label": "Execution", "folder": "lab/09_execution", "description": "Bridge, logging, and execution design notes."},
    {"stage_id": "infrastructure", "label": "Infrastructure", "folder": "lab/10_infrastructure", "description": "CI, configuration, data and utility documentation."},
    {"stage_id": "core", "label": "Core Engines", "folder": "lab/core", "description": "Market data, structural nodes, metrics, and engine modules."},
    {"stage_id": "docs", "label": "Project Docs", "folder": "docs", "description": "Manifesto, principles, architecture, glossary, roadmap, and UI contracts."},
]

ID_RE = re.compile(r"\b(OBS\d+|H\d+|M\d+|EXP\d+|ANL\d+|VAL\d+|SIG\d+|MON\d+|CP\d+)\b", re.IGNORECASE)
STATUS_RE = re.compile(r"^\s*(?:##\s*)?Status\s*[:\-]?\s*(.+)$", re.IGNORECASE | re.MULTILINE)
TITLE_RE = re.compile(r"^#\s+(.+)$", re.MULTILINE)


@dataclass(frozen=True)
class LabDoc:
    doc_id: str
    title: str
    stage_id: str
    stage_label: str
    path: str
    extension: str
    status: str | None
    summary: str
    relation_ids: list[str]
    size_bytes: int
    modified_time: float


def safe_relative_path(path: str) -> Path:
    root = settings.root_path.resolve()
    candidate = (root / path).resolve()
    if root not in candidate.parents and candidate != root:
        raise ValueError("Path escapes repository root")
    return candidate


def list_stages() -> list[dict[str, object]]:
    docs = list_documents()
    counts: dict[str, int] = {}
    for doc in docs:
        counts[doc.stage_id] = counts.get(doc.stage_id, 0) + 1
    return [{**stage, "count": counts.get(stage["stage_id"], 0)} for stage in STAGES]


def list_documents(stage_id: str | None = None, query: str | None = None) -> list[LabDoc]:
    root = settings.root_path
    docs: list[LabDoc] = []
    wanted = {stage_id} if stage_id else None
    needle = query.lower().strip() if query else None

    for stage in STAGES:
        if wanted and stage["stage_id"] not in wanted:
            continue
        folder = root / stage["folder"]
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in DOC_EXTENSIONS:
                continue
            try:
                doc = build_doc(path, stage)
            except UnicodeDecodeError:
                continue
            searchable = f"{doc.doc_id} {doc.title} {doc.path} {doc.summary} {doc.status or ''}".lower()
            if needle and needle not in searchable:
                continue
            docs.append(doc)
    return docs


def read_document(path: str) -> dict[str, object]:
    candidate = safe_relative_path(path)
    if not candidate.exists() or not candidate.is_file():
        raise FileNotFoundError(path)
    if candidate.suffix.lower() not in DOC_EXTENSIONS:
        raise ValueError("Unsupported document type")

    content = candidate.read_text(encoding="utf-8", errors="replace")
    stage = stage_for_path(candidate)
    doc = build_doc(candidate, stage)
    return {
        "doc": doc_to_dict(doc),
        "content": content,
        "outline": extract_outline(content),
        "front_matter": extract_front_matter(content),
    }


def overview() -> dict[str, object]:
    docs = list_documents()
    stage_rows = list_stages()
    hypotheses = [doc for doc in docs if doc.stage_id == "hypotheses"]
    experiments = [doc for doc in docs if doc.stage_id == "experiments"]
    validations = [doc for doc in docs if doc.stage_id == "validation"]
    metrics = [doc for doc in docs if doc.doc_id.startswith("M")]

    return {
        "stages": stage_rows,
        "stats": {
            "documents": len(docs),
            "hypotheses": len(hypotheses),
            "experiments": len(experiments),
            "validations": len(validations),
            "metrics": len(metrics),
        },
        "lineage": build_lineage(docs),
        "critical_path": [
            {"id": "OBS0001", "label": "Structural highs/lows", "stage": "Observation"},
            {"id": "H0001", "label": "Decision nodes", "stage": "Hypothesis"},
            {"id": "H0002", "label": "Node territories", "stage": "Hypothesis"},
            {"id": "M0001", "label": "Relative Territory Volatility", "stage": "Metric"},
            {"id": "EXP0001", "label": "Real market inspection", "stage": "Experiment"},
            {"id": "VAL001", "label": "Validation gate", "stage": "Validation"},
            {"id": "SIG001", "label": "Production signal candidate", "stage": "Production"},
        ],
    }


def build_doc(path: Path, stage: dict[str, str]) -> LabDoc:
    rel = path.relative_to(settings.root_path).as_posix()
    content = read_preview(path)
    title = extract_title(content) or title_from_path(path)
    doc_id = extract_doc_id(path.name, content)
    status = extract_status(content)
    summary = extract_summary(content)
    relation_ids = sorted({match.upper() for match in ID_RE.findall(content) if match.upper() != doc_id})[:16]
    stat = path.stat()
    return LabDoc(
        doc_id=doc_id,
        title=title,
        stage_id=stage["stage_id"],
        stage_label=stage["label"],
        path=rel,
        extension=path.suffix.lower().lstrip("."),
        status=status,
        summary=summary,
        relation_ids=relation_ids,
        size_bytes=stat.st_size,
        modified_time=stat.st_mtime,
    )


def stage_for_path(path: Path) -> dict[str, str]:
    rel = path.relative_to(settings.root_path).as_posix()
    for stage in STAGES:
        if rel == stage["folder"] or rel.startswith(stage["folder"].rstrip("/") + "/"):
            return stage
    return {"stage_id": "unknown", "label": "Unknown", "folder": "", "description": ""}


def doc_to_dict(doc: LabDoc) -> dict[str, object]:
    return {
        "doc_id": doc.doc_id,
        "title": doc.title,
        "stage_id": doc.stage_id,
        "stage_label": doc.stage_label,
        "path": doc.path,
        "extension": doc.extension,
        "status": doc.status,
        "summary": doc.summary,
        "relation_ids": doc.relation_ids,
        "size_bytes": doc.size_bytes,
        "modified_time": doc.modified_time,
    }


def docs_to_dicts(docs: Iterable[LabDoc]) -> list[dict[str, object]]:
    return [doc_to_dict(doc) for doc in docs]


def read_preview(path: Path, max_chars: int = 12000) -> str:
    return path.read_text(encoding="utf-8", errors="replace")[:max_chars]


def extract_title(content: str) -> str | None:
    match = TITLE_RE.search(content)
    if match:
        return match.group(1).strip().strip("#")
    return None


def title_from_path(path: Path) -> str:
    return path.stem.replace("_", " ").replace("-", " ").strip().title()


def extract_doc_id(name: str, content: str) -> str:
    for source in (name, content[:500]):
        match = ID_RE.search(source)
        if match:
            return match.group(1).upper()
    return Path(name).stem.upper().replace("-", "_")


def extract_status(content: str) -> str | None:
    match = STATUS_RE.search(content)
    if not match:
        return None
    return match.group(1).strip().strip("*` ")[:80]


def extract_summary(content: str) -> str:
    lines = []
    in_code = False
    for raw in content.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line or line.startswith("#") or line.startswith("---"):
            continue
        if line.startswith(("*", "-")):
            line = line[1:].strip()
        lines.append(line)
        if len(" ".join(lines)) > 260:
            break
    return " ".join(lines)[:320]


def extract_outline(content: str) -> list[dict[str, object]]:
    outline = []
    for line in content.splitlines():
        if not line.startswith("#"):
            continue
        level = len(line) - len(line.lstrip("#"))
        if level > 4:
            continue
        title = line.lstrip("#").strip()
        if title:
            outline.append({"level": level, "title": title})
    return outline[:80]


def extract_front_matter(content: str) -> dict[str, str]:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    result: dict[str, str] = {}
    for raw in parts[1].splitlines():
        if ":" not in raw:
            continue
        key, value = raw.split(":", 1)
        result[key.strip()] = value.strip().strip('"\'')
    return result


def build_lineage(docs: list[LabDoc]) -> list[dict[str, object]]:
    docs_by_id = {doc.doc_id: doc for doc in docs}
    nodes = []
    for doc in docs:
        nodes.append({
            "id": doc.doc_id,
            "title": doc.title,
            "stage_id": doc.stage_id,
            "path": doc.path,
            "status": doc.status,
            "relations": [relation for relation in doc.relation_ids if relation in docs_by_id],
        })
    return nodes
