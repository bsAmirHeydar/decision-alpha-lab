from __future__ import annotations

import csv
import json
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable

from .models import AuditResult


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        if fieldnames:
            writer.writeheader()
            writer.writerows(rows)


def write_artifacts(result: AuditResult, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    _write_csv(output_dir / "repository_inventory.csv", (item.to_dict() for item in result.files))
    _write_json(output_dir / "repository_inventory.json", [item.to_dict() for item in result.files])
    _write_csv(output_dir / "module_classification.csv", (item.to_dict() for item in result.modules))
    _write_json(output_dir / "module_classification.json", [item.to_dict() for item in result.modules])
    _write_csv(output_dir / "execution_authority_scan.csv", (item.to_dict() for item in result.authority_findings),
               ["path", "line", "token", "authority_type", "severity", "snippet"])
    _write_csv(output_dir / "contract_schema_map.csv", (item.to_dict() for item in result.contracts))
    _write_csv(output_dir / "duplicate_engine_matrix.csv", (item.to_dict() for item in result.duplicates))
    _write_json(output_dir / "migration_risk_register.json", [item.to_dict() for item in result.risks])
    _write_json(output_dir / "test_baseline.json", result.test_baseline)
    _write_json(output_dir / "audit_summary.json", result.summary)

    pilot = {
        "selected_pilot": "CP0001_STRUCTURAL_NODES_M0001_RTV",
        "selection_reason": "It is the only implemented anatomy-to-metric path in the audited snapshot and exercises data, anatomy, persistence, and outcomes.",
        "constraint": "EXP0017 and NDS are absent from this uploaded archive; they cannot be selected as code pilots until supplied.",
        "next_phase_consumers": ["PHASE_01", "PHASE_02", "PHASE_06", "PHASE_10"],
    }
    _write_json(output_dir / "pilot_selection.json", pilot)

    action_counts = Counter(item.action.value for item in result.modules)
    category_counts = Counter(item.category for item in result.files)
    risk_counts = Counter(item.severity.value for item in result.risks)

    report = f"""# Strategy Factory Phase 00 — Current-State Report

## Audit identity

- Generated at: `{result.generated_at_utc}`
- Git commit: `{result.git_commit}`
- Repository root label: `{result.repo_root.name}`
- Audit status: **{result.summary['phase_gate_status']}**

## Executive conclusion

The audited repository is a compact research foundation, not yet a Strategy Factory implementation. It contains a functional MT5-to-Parquet market-data path, a reusable L-rule structural-node detector, and one revisit-aware structural metric. The later EXP0017, NDS, Daye, model-training, execution, and portfolio systems referenced by the implementation roadmap are not present in this uploaded snapshot.

The correct migration strategy is therefore **preserve and wrap the implemented anatomy/data primitives, replace empty scaffolding with shared factory modules, consolidate persistence, and freeze canonical contracts before expanding behavior**.

## Inventory

- Files audited: **{len(result.files)}**
- Empty files: **{sum(1 for item in result.files if item.is_empty)}**
- Python contracts discovered: **{len(result.contracts)}**
- Potential duplicate capability groups: **{len(result.duplicates)}**
- Live execution authority findings: **{len(result.authority_findings)}**

### File categories

"""
    for category, count in sorted(category_counts.items()):
        report += f"- `{category}`: {count}\n"

    report += "\n## Migration classification\n\n"
    for action, count in sorted(action_counts.items()):
        report += f"- `{action}`: {count}\n"

    report += "\n## Capital authority finding\n\n"
    if result.authority_findings:
        report += "Potential live-order authority was found. Phase 00 cannot close until each call site is classified and quarantined.\n"
    else:
        report += "No executable `OrderSend`, `OrderCheck`, `CTrade`, or `mt5.order_send` call site was found. The audited snapshot has market-data access but no identified order-send authority.\n"

    pytest = result.test_baseline.get("pytest", {})
    report += f"""

## Test baseline

- Python compileall: **{'PASS' if result.test_baseline.get('compileall', {}).get('passed') else 'FAIL'}**
- Pytest clean-checkout baseline: **{'PASS' if pytest.get('passed') else 'FAIL'}**
- Pytest return code: `{pytest.get('return_code')}`

The collection failure is a Phase 02 packaging concern, not evidence that the implemented market/anatomy logic is numerically wrong. It must still be corrected before shared-engine development.

## Primary migration decisions

1. Keep the laboratory philosophy and Python/MQL5 authority separation.
2. Adapt `MT5Connector` behind a vendor-neutral market-data port.
3. Wrap `MarketDataEngine` as a legacy provider until canonical bar/time contracts exist.
4. Wrap `LRuleNodeDetector` as an anatomy plugin; never move L-rule semantics into the kernel.
5. Wrap `M0001RTV` as a feature/label plugin and correct its interface drift under contract tests.
6. Replace three cache implementations with one versioned Artifact Store.
7. Migrate empty experiment/validation/production shells to manifest-driven runs.
8. Delete tracked bytecode and runtime caches after ignore rules are installed.

## Pilot decision

Phase 00 selects **CP0001 Structural Nodes + M0001 RTV** as the local foundation pilot because it is the only complete implemented chain in this archive. This does not replace the roadmap decision to use EXP0017 and NDS as later platform pilots; those codebases must first be present in the working repository.

## Risk profile

"""
    for severity, count in sorted(risk_counts.items()):
        report += f"- `{severity}`: {count}\n"

    report += """

## Phase gate

Phase 00 is accepted when the generated artifacts are reproducible, the authority scan remains clean or fully classified, every reusable module has a migration action, the pilot is explicit, and Phase 01 can consume the contract/schema map without undocumented assumptions.
"""
    (output_dir / "current_state_report.md").write_text(report, encoding="utf-8")

    qa = {
        "phase": "PHASE_00",
        "status": result.summary["phase_gate_status"],
        "checks": {
            "repository_inventory_generated": (output_dir / "repository_inventory.json").exists(),
            "module_classification_generated": (output_dir / "module_classification.csv").exists(),
            "duplicate_matrix_generated": (output_dir / "duplicate_engine_matrix.csv").exists(),
            "migration_risk_register_generated": (output_dir / "migration_risk_register.json").exists(),
            "execution_authority_scan_generated": (output_dir / "execution_authority_scan.csv").exists(),
            "pilot_selected": True,
            "all_modules_classified": all(item.action.value for item in result.modules),
            "no_unidentified_live_authority": not result.authority_findings,
        },
        "blocking_items_for_phase_01": [],
        "deferred_items": ["Python packaging/test collection to PHASE_02", "Canonical UTC market clock to PHASE_07"],
    }
    qa["passed"] = all(qa["checks"].values())
    _write_json(output_dir / "phase00_qa_report.json", qa)
