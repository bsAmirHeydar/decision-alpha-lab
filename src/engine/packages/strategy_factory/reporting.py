"""Human-readable Markdown reporting for standard Strategy Factory runs."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import pandas as pd

from .statistics import PerformanceSummary


def _table(mapping: Mapping[str, Any]) -> str:
    lines = ["| Metric | Value |", "|---|---:|"]
    for key, value in mapping.items():
        if isinstance(value, float):
            rendered = f"{value:.6f}"
        else:
            rendered = str(value)
        lines.append(f"| `{key}` | {rendered} |")
    return "\n".join(lines)


def write_run_report(
    path: str | Path,
    *,
    title: str,
    run_manifest: Mapping[str, Any],
    performance: PerformanceSummary,
    anti_overfit: Mapping[str, Any],
    limitations: Sequence[str],
    promotion_status: str,
) -> Path:
    resolved = Path(path)
    resolved.parent.mkdir(parents=True, exist_ok=True)
    body = f"""---
type: strategy-factory-run-report
status: generated
run_id: {run_manifest.get('run_id')}
strategy_id: {run_manifest.get('strategy_id')}
---

# {title}

## Research identity

{_table(run_manifest)}

## Performance summary

{_table(performance.to_dict())}

## Anti-overfit evidence

{_table(anti_overfit)}

## Promotion status

`{promotion_status}`

## Known limitations

"""
    for item in limitations:
        body += f"- {item}\n"
    body += "\n## Authority boundary\n\nThis report is evidence. It does not authorize live execution or risk scaling.\n"
    resolved.write_text(body, encoding="utf-8")
    return resolved
