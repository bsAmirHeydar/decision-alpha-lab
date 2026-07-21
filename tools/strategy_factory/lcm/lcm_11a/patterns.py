from __future__ import annotations
import re

CALL_TOKENS = ("ObjectCreate", "SetIndexBuffer")
REPORT_TOKENS = ("savefig", "write_html", "to_html", "dashboard_rows")
DELETE_TOKENS = ("ObjectsDeleteAll", "ObjectDelete")

FUNCTION_PATTERNS = (
    re.compile(r"(?:^|\s)(?:void|bool|int|long|double|string|datetime|color|ENUM_[A-Z0-9_]+|[A-Z][A-Za-z0-9_<>:]*)\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("),
    re.compile(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\("),
)

def nearest_function(lines: list[str], line_index: int) -> str:
    for idx in range(line_index, max(-1, line_index - 160), -1):
        line = lines[idx]
        for pattern in FUNCTION_PATTERNS:
            match = pattern.search(line)
            if match:
                return match.group(1)
    return "GLOBAL_SCOPE"

def extract_balanced_call(text: str, token_start: int) -> tuple[str, int] | None:
    open_at = text.find("(", token_start)
    if open_at < 0:
        return None
    depth = 0; quote = None; escaped = False
    for idx in range(open_at, len(text)):
        ch = text[idx]
        if escaped:
            escaped = False; continue
        if ch == "\\":
            escaped = True; continue
        if quote:
            if ch == quote: quote = None
            continue
        if ch in ("'", '"'):
            quote = ch; continue
        if ch == "(": depth += 1
        elif ch == ")":
            depth -= 1
            if depth == 0:
                return text[open_at + 1:idx], idx + 1
    return None

def split_arguments(raw: str) -> list[str]:
    args=[]; start=0; depth=0; quote=None; escaped=False
    for idx,ch in enumerate(raw):
        if escaped:
            escaped=False; continue
        if ch == "\\":
            escaped=True; continue
        if quote:
            if ch == quote: quote=None
            continue
        if ch in ("'", '"'):
            quote=ch; continue
        if ch in "([{<": depth += 1
        elif ch in ")]}>": depth=max(0,depth-1)
        elif ch == "," and depth == 0:
            args.append(raw[start:idx].strip()); start=idx+1
    args.append(raw[start:].strip())
    return args
