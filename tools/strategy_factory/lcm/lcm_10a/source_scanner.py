from __future__ import annotations

from pathlib import Path
from typing import Iterable

from .canonical import file_digest
from .constants import (
    EXCLUDED_PARTS,
    GENERATED_EXCLUDED_PREFIXES,
    SOURCE_ROOTS,
    SOURCE_SUFFIXES,
)
from .models import SourceAnalysis, sorted_unique
from .patterns import (
    CAPABILITY_PATTERNS,
    MODE_PATTERNS,
    RISK_PATTERNS,
    TREATMENT_PATTERNS,
)

DEEP_SCAN_TOKENS = (
    "ordersend", "ctrade", "positionopen", "positionmodify", "positionclose",
    "orderdelete", "ordermodify", "buylimit", "selllimit", "buystop", "sellstop",
    "mqltraderequest", "ordercheck", "positionselect", "positionget", "positionstotal",
    "orderselect", "ordersget", "orderstotal", "historyselect", "historydeal", "historyorder",
    "symbolinfo", "accountinfo", "fileopen", "filewrite", "filedelete", "webrequest",
    "socketcreate", "stop_loss", "stoploss", "take_profit", "takeprofit", "target_price",
    "entry_price", "risk_percent", "risk_pct", "volume_step", "partial_exit",
    "partial_close", "breakeven", "break_even", "trailing", "trail_stop",
    "time_exit", "expiry", "expiration", "slippage", "deviation_points",
    "tick_size", "tick_value", "stops_level", "freeze_level", "spread",
    "market_entry", "limit_order", "stop_order", "order_type_buy", "order_type_sell",
    "paper_broker", "dry_run", "no_send", "live_mode", "reconcile",
)

from .text_analysis import (
    containing_symbol,
    line_evidence,
    mql_functions,
    python_functions,
    strip_mql_comments,
)


def _eligible(repo_root: Path, path: Path) -> bool:
    relative = path.relative_to(repo_root).as_posix()
    if any(part in EXCLUDED_PARTS for part in path.parts):
        return False
    if any(relative.startswith(prefix) for prefix in GENERATED_EXCLUDED_PREFIXES):
        return False
    return path.suffix.lower() in SOURCE_SUFFIXES


def discover_sources(repo_root: Path) -> list[Path]:
    paths: list[Path] = []
    for relative in SOURCE_ROOTS:
        base = repo_root / relative
        if base.is_dir():
            paths.extend(
                path
                for path in base.rglob("*")
                if path.is_file() and _eligible(repo_root, path)
            )
    return sorted(
        set(paths),
        key=lambda path: path.relative_to(repo_root).as_posix().lower(),
    )


def _language(path: Path) -> str:
    if path.suffix.lower() in {".mq5", ".mqh"}:
        return "MQL5"
    if path.suffix.lower() == ".py":
        return "PYTHON"
    return "CONFIG"


def _mode_classes(path: str, text: str, capability_codes: list[str]) -> list[str]:
    modes: list[str] = []
    combined = path + "\n" + text[:200000]
    for name, pattern in MODE_PATTERNS:
        if pattern.search(combined):
            modes.append(name)
    if any(
        code.startswith("BROKER_SUBMIT")
        or code
        in {
            "BROKER_POSITION_OPEN",
            "BROKER_POSITION_MODIFY",
            "BROKER_ORDER_MODIFY",
            "BROKER_ORDER_CANCEL",
            "BROKER_POSITION_CLOSE",
        }
        for code in capability_codes
    ):
        modes.append("LIVE_CAPABLE_SURFACE")
    return sorted_unique(modes or ["MODE_NOT_EXPLICIT"])


def _scan_patterns(
    path: str,
    text: str,
    functions: list,
    specs: Iterable,
    kind: str,
) -> list[dict]:
    clean = strip_mql_comments(text) if path.lower().endswith((".mq5", ".mqh")) else text
    clean_lines = clean.splitlines()
    original_lines = text.splitlines()
    hits: list[dict] = []
    for line_number, line in enumerate(clean_lines, 1):
        stripped = line.strip()
        if not stripped or (path.lower().endswith(".py") and stripped.startswith("#")):
            continue
        symbol = containing_symbol(functions, line_number)
        for spec in specs:
            matches = list(spec.expression.finditer(line))
            if not matches:
                continue
            original = original_lines[line_number - 1] if line_number <= len(original_lines) else line
            evidence = line_evidence(path, line_number, original, symbol)
            hits.append(
                {
                    "evidence_kind": kind,
                    "pattern_code": spec.code,
                    "authority_class": spec.authority_class,
                    "severity": spec.severity,
                    "match_count_on_line": len(matches),
                    **evidence,
                }
            )
    hits.sort(
        key=lambda row: (
            row["path"],
            row["line_number"],
            row["pattern_code"],
            row.get("symbol_id") or "",
        )
    )
    return hits


def scan_source(repo_root: Path, path: Path) -> SourceAnalysis:
    relative = path.relative_to(repo_root).as_posix()
    language = _language(path)
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    functions = []
    parse_error = None
    lower_text = text.lower()
    deep_scan = any(token in lower_text for token in DEEP_SCAN_TOKENS)
    if deep_scan and language == "MQL5":
        functions = mql_functions(relative, text)
    elif deep_scan and language == "PYTHON":
        functions, parse_error = python_functions(relative, text)
    if not deep_scan:
        return SourceAnalysis(
            path=relative, language=language, sha256=file_digest(path), size_bytes=len(raw),
            line_count=text.count("\n") + (1 if text else 0), mode_classes=["MODE_NOT_EVALUATED_NO_RELEVANT_TOKEN"],
            functions=[], treatment_hits=[], capability_hits=[], risk_hits=[], parse_status="PASS", parse_error=None,
        )
    treatments = _scan_patterns(
        relative,
        text,
        functions,
        TREATMENT_PATTERNS,
        "TREATMENT_ATOM",
    )
    capabilities = _scan_patterns(
        relative,
        text,
        functions,
        CAPABILITY_PATTERNS,
        "EXECUTION_CAPABILITY",
    )
    risks = _scan_patterns(
        relative,
        text,
        functions,
        RISK_PATTERNS,
        "RISK_ASSUMPTION",
    )
    return SourceAnalysis(
        path=relative,
        language=language,
        sha256=file_digest(path),
        size_bytes=len(raw),
        line_count=text.count("\n") + (1 if text else 0),
        mode_classes=_mode_classes(
            relative,
            text,
            [row["pattern_code"] for row in capabilities],
        ),
        functions=functions,
        treatment_hits=treatments,
        capability_hits=capabilities,
        risk_hits=risks,
        parse_status="PASS" if parse_error is None else "UNKNOWN_PARSE",
        parse_error=parse_error,
    )


def scan_repository(repo_root: Path) -> list[SourceAnalysis]:
    return [scan_source(repo_root, path) for path in discover_sources(repo_root)]
