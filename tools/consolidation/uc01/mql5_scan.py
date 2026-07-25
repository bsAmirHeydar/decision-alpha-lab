"""Conservative MQL5/MQH inventory and authority-surface scanner."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Iterable

from .classification import critical_domains, owner_domain
from .io_utils import safe_read_text

_INCLUDE_RE = re.compile(r"^\s*#include\s*[<\"]([^>\"]+)[>\"]", re.MULTILINE)
_CLASS_RE = re.compile(r"\b(class|struct|enum)\s+([A-Za-z_][A-Za-z0-9_]*)")
_FUNCTION_RE = re.compile(
    r"(?m)^\s*(?:(?:static|virtual|const|inline|template)\s+)*"
    r"([A-Za-z_][A-Za-z0-9_:<>\[\]]*(?:\s*\*)?)\s+"
    r"([A-Za-z_][A-Za-z0-9_:]*)\s*\(([^;{}]*)\)\s*(?:const\s*)?(?=\{|;)",
)
_INPUT_RE = re.compile(r"(?m)^\s*(input|sinput)\s+([A-Za-z_][A-Za-z0-9_:<>\[\]]*)\s+([A-Za-z_][A-Za-z0-9_]*)")
_DEFINE_RE = re.compile(r"(?m)^\s*#define\s+([A-Za-z_][A-Za-z0-9_]*)")
_IMPORT_RE = re.compile(r"(?m)^\s*#import\s+[\"<]([^\">]+)[\">]")

_AUTHORITY_TOKENS = {
    "order_send": ("OrderSend", "OrderSendAsync"),
    "trade_class": ("CTrade",),
    "position_mutation": ("PositionOpen", "PositionClose", "PositionModify"),
    "pending_order": ("BuyLimit", "SellLimit", "BuyStop", "SellStop", "OrderDelete"),
    "network": ("WebRequest",),
    "dll": ("#import",),
    "filesystem_write": ("FileWrite", "FileWriteArray", "FileWriteString", "FileDelete", "FileMove"),
    "terminal_global_state": ("GlobalVariableSet", "GlobalVariablesDeleteAll"),
}


def scan_mql5(repo_root: Path, mql_paths: Iterable[str]) -> dict[str, list[dict]]:
    symbols: list[dict] = []
    includes: list[dict] = []
    authority: list[dict] = []
    issues: list[dict] = []
    for rel_path in sorted(set(mql_paths)):
        path = repo_root / rel_path
        text, issue = safe_read_text(path, max_bytes=24 * 1024 * 1024)
        if text is None:
            issues.append({"path": rel_path, "issue": issue or "unreadable"})
            continue
        for match in _INCLUDE_RE.finditer(text):
            includes.append({
                "source_path": rel_path,
                "target_include": match.group(1).replace("\\", "/"),
                "line": text.count("\n", 0, match.start()) + 1,
            })
        for kind, name in _CLASS_RE.findall(text):
            symbols.append(_symbol_row(rel_path, kind, name, text, name))
        for return_type, name, args in _FUNCTION_RE.findall(text):
            symbols.append(_symbol_row(rel_path, "function", name, text, f"{return_type} {name}({args})", {
                "return_type": return_type.strip(),
                "signature": " ".join(args.split()),
            }))
        for qualifier, value_type, name in _INPUT_RE.findall(text):
            symbols.append(_symbol_row(rel_path, "input", name, text, f"{qualifier} {value_type} {name}", {
                "value_type": value_type,
                "qualifier": qualifier,
            }))
        for name in _DEFINE_RE.findall(text):
            symbols.append(_symbol_row(rel_path, "macro", name, text, f"#define {name}"))
        for imported in _IMPORT_RE.findall(text):
            symbols.append(_symbol_row(rel_path, "external_import", imported, text, f"#import {imported}"))
        for authority_kind, tokens in _AUTHORITY_TOKENS.items():
            hits = []
            for token in tokens:
                for match in re.finditer(rf"\b{re.escape(token)}\b", text):
                    hits.append({"token": token, "line": text.count("\n", 0, match.start()) + 1})
            if hits:
                authority.append({
                    "path": rel_path,
                    "authority_kind": authority_kind,
                    "hits": hits,
                    "owner_domain": owner_domain(rel_path),
                })
        if not any(row["path"] == rel_path for row in symbols):
            symbols.append(_symbol_row(rel_path, "module", Path(rel_path).stem, text, text))
    return {
        "symbols": sorted(symbols, key=lambda x: (x["path"], x["kind"], x["name"])),
        "includes": sorted(includes, key=lambda x: (x["source_path"], x["line"], x["target_include"])),
        "authority": sorted(authority, key=lambda x: (x["path"], x["authority_kind"])),
        "issues": sorted(issues, key=lambda x: x["path"]),
    }


def _symbol_row(rel_path: str, kind: str, name: str, text: str, surface: str, extra: dict | None = None) -> dict:
    row = {
        "path": rel_path,
        "kind": kind,
        "name": name,
        "owner_domain": owner_domain(rel_path),
        "critical_domains": critical_domains(rel_path, name),
        "surface_sha256": hashlib.sha256(surface.encode("utf-8", errors="replace")).hexdigest(),
    }
    if extra:
        row.update(extra)
    return row
