from __future__ import annotations

import re
from pathlib import Path

from .models import AuthorityFinding, Severity
from .scope import is_phase00_self_path


PATTERNS: tuple[tuple[str, str, Severity, re.Pattern[str]], ...] = (
    ("MQL5_ORDER_SEND", "live_order_send", Severity.CRITICAL, re.compile(r"\bOrderSend\s*\(")),
    ("MQL5_ORDER_CHECK", "live_order_preflight", Severity.HIGH, re.compile(r"\bOrderCheck\s*\(")),
    ("MQL5_CTRADE", "live_trade_wrapper", Severity.HIGH, re.compile(r"\bCTrade\b")),
    ("PY_MT5_ORDER_SEND", "live_order_send", Severity.CRITICAL, re.compile(r"\bmt5\.order_send\s*\(")),
    ("PY_MT5_ORDER_CHECK", "live_order_preflight", Severity.HIGH, re.compile(r"\bmt5\.order_check\s*\(")),
    ("BROKER_BUY_SELL", "potential_order_send", Severity.HIGH, re.compile(r"\.(?:buy|sell|submit_order|place_order)\s*\(")),
)

SCAN_SUFFIXES = {".py", ".mq5", ".mqh", ".cpp", ".h", ".ps1"}


def scan_execution_authority(repo_root: Path) -> list[AuthorityFinding]:
    findings: list[AuthorityFinding] = []
    for path in sorted(repo_root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SCAN_SUFFIXES:
            continue
        if ".git" in path.parts or "__pycache__" in path.parts:
            continue
        relative = path.relative_to(repo_root).as_posix()
        if is_phase00_self_path(relative):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or stripped.startswith("//"):
                continue
            for token, authority_type, severity, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append(
                        AuthorityFinding(
                            path=relative,
                            line=line_number,
                            token=token,
                            authority_type=authority_type,
                            severity=severity,
                            snippet=stripped[:240],
                        )
                    )
    return findings
