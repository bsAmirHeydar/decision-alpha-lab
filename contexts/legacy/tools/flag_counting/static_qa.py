#!/usr/bin/env python3
"""Phoenix Flag Counting static QA scanner.

This script is intentionally dependency-free. It scans the Phoenix MQL5 source
for the compile-risk patterns that repeatedly caused breakage while the layered
engine was being built:

- empty Print() calls
- very long multi-argument Print(...) calls
- duplicate input names in the Phoenix EA
- stale identity_generation_pass values
- stale interface contract versions
- common stale short report references such as r.export_forced
- missing Level 18 public modules

Usage:
  python contexts/legacy/tools/flag_counting/static_qa.py --root .
  python contexts/legacy/tools/flag_counting/static_qa.py --root . --csv reports/static_qa.csv
  python contexts/legacy/tools/flag_counting/static_qa.py --root . --strict
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

EXPECTED_ID_PASS = "phoenix_level18"
EXPECTED_INTERFACE_VERSION = "18.00"
PHOENIX_INCLUDE = Path("mql5/Include/FlagCountingPhoenix")
PHOENIX_EA = Path("mql5/Experts/FlagCounting/FlagCountingPhoenixExperiment.mq5")
REQUIRED_LEVEL18_MODULES = [
    "FP_StaticQaTypes.mqh",
    "FP_StaticQaRules.mqh",
    "FP_StaticQaAudit.mqh",
    "FP_StaticQaEngine.mqh",
]

@dataclass
class Finding:
    severity: str
    check_id: str
    path: str
    line: int
    status: str
    detail: str


def iter_mql_files(root: Path) -> Iterable[Path]:
    base = root / PHOENIX_INCLUDE
    if base.exists():
        yield from sorted(base.glob("*.mqh"))
    ea = root / PHOENIX_EA
    if ea.exists():
        yield ea


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"//.*", "", text)
    return text


def line_no(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def split_args(arg_text: str) -> List[str]:
    args: List[str] = []
    depth = 0
    quote = False
    escape = False
    start = 0
    for i, ch in enumerate(arg_text):
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                quote = False
            continue
        if ch == '"':
            quote = True
        elif ch in "([{" :
            depth += 1
        elif ch in ")]}":
            depth = max(0, depth - 1)
        elif ch == "," and depth == 0:
            args.append(arg_text[start:i].strip())
            start = i + 1
    tail = arg_text[start:].strip()
    if tail:
        args.append(tail)
    return args


def find_print_calls(path: Path, rel: str, findings: List[Finding]) -> None:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    text = strip_comments(raw)
    for m in re.finditer(r"\bPrint\s*\(", text):
        start = m.end()
        depth = 1
        i = start
        quote = False
        escape = False
        while i < len(text) and depth > 0:
            ch = text[i]
            if quote:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    quote = False
            else:
                if ch == '"':
                    quote = True
                elif ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
            i += 1
        args = text[start:i-1].strip()
        n = len(split_args(args)) if args else 0
        ln = line_no(text, m.start())
        if n == 0:
            findings.append(Finding("error", "EMPTY_PRINT", rel, ln, "FAIL", "Print() has no arguments"))
        elif n > 20:
            findings.append(Finding("warn", "LONG_PRINT_ARGS", rel, ln, "WARN", f"Print has {n} top-level arguments; prefer one prebuilt string"))


def check_duplicate_inputs(root: Path, findings: List[Finding]) -> None:
    path = root / PHOENIX_EA
    if not path.exists():
        findings.append(Finding("error", "EA_PRESENT", str(PHOENIX_EA), 0, "FAIL", "Phoenix EA is missing"))
        return
    text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
    names = re.findall(r"^\s*input\s+[^;=]+?\s+(Inp[A-Za-z0-9_]+)\b", text, flags=re.M)
    seen = set()
    for name in names:
        if name in seen:
            findings.append(Finding("error", "DUPLICATE_INPUT", str(PHOENIX_EA), 0, "FAIL", f"duplicate input {name}"))
        seen.add(name)
    if names:
        findings.append(Finding("info", "INPUT_COUNT", str(PHOENIX_EA), 0, "PASS", f"{len(names)} input declarations scanned"))


def check_identity_and_versions(root: Path, findings: List[Finding]) -> None:
    stale = []
    for path in iter_mql_files(root):
        rel = str(path.relative_to(root))
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "phoenix_level17" in text or "phoenix_level16" in text:
            # Documentation strings in old docs are not scanned here; MQL source must be current.
            stale.append(rel)
    if stale:
        findings.append(Finding("error", "STALE_IDENTITY_PASS", ";".join(stale), 0, "FAIL", "stale phoenix_level16/17 references in MQL source"))
    else:
        findings.append(Finding("info", "IDENTITY_PASS_CURRENT", str(PHOENIX_INCLUDE), 0, "PASS", EXPECTED_ID_PASS))

    iface = root / PHOENIX_INCLUDE / "FP_InterfaceTypes.mqh"
    if iface.exists():
        text = iface.read_text(encoding="utf-8", errors="ignore")
        if f'FP_INTERFACE_CONTRACT_VERSION "{EXPECTED_INTERFACE_VERSION}"' not in text:
            findings.append(Finding("error", "INTERFACE_VERSION", str(iface.relative_to(root)), 0, "FAIL", f"expected {EXPECTED_INTERFACE_VERSION}"))
        else:
            findings.append(Finding("info", "INTERFACE_VERSION", str(iface.relative_to(root)), 0, "PASS", EXPECTED_INTERFACE_VERSION))


def check_required_modules(root: Path, findings: List[Finding]) -> None:
    for mod in REQUIRED_LEVEL18_MODULES:
        p = root / PHOENIX_INCLUDE / mod
        findings.append(Finding("error" if not p.exists() else "info", "LEVEL18_MODULE", str(PHOENIX_INCLUDE / mod), 0, "PASS" if p.exists() else "FAIL", "required Level 18 module"))


def check_stale_report_aliases(root: Path, findings: List[Finding]) -> None:
    pattern = re.compile(r"\br\.(export_forced|render_suppressed|validation_forced|rollback_safe_mode)\b")
    for path in iter_mql_files(root):
        rel = str(path.relative_to(root))
        text = strip_comments(path.read_text(encoding="utf-8", errors="ignore"))
        for m in pattern.finditer(text):
            findings.append(Finding("warn", "SHORT_REPORT_ALIAS", rel, line_no(text, m.start()), "WARN", m.group(0)))


def run(root: Path) -> List[Finding]:
    findings: List[Finding] = []
    for path in iter_mql_files(root):
        find_print_calls(path, str(path.relative_to(root)), findings)
    check_duplicate_inputs(root, findings)
    check_identity_and_versions(root, findings)
    check_required_modules(root, findings)
    check_stale_report_aliases(root, findings)
    if not any(f.status == "FAIL" for f in findings):
        findings.append(Finding("info", "STATIC_QA_OK", ".", 0, "PASS", "no blocking static QA findings"))
    return findings


def write_csv(path: Path, findings: List[Finding]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["severity", "check_id", "path", "line", "status", "detail"])
        for item in findings:
            w.writerow([item.severity, item.check_id, item.path, item.line, item.status, item.detail])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--csv", default="", help="optional CSV output path")
    parser.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    findings = run(root)
    if args.csv:
        write_csv(Path(args.csv), findings)
    for item in findings:
        print(f"{item.status}\t{item.severity}\t{item.check_id}\t{item.path}:{item.line}\t{item.detail}")
    has_error = any(f.status == "FAIL" for f in findings)
    has_warn = any(f.status == "WARN" for f in findings)
    return 1 if has_error or (args.strict and has_warn) else 0

if __name__ == "__main__":
    raise SystemExit(main())
