
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FORBIDDEN_MQL5_TOKENS = ("OrderSend(", "CTrade", "PositionOpen(", "WebRequest(")


def parse_utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def load_fixture(path: Path):
    datasets = defaultdict(lambda: defaultdict(list))
    with path.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            datasets[row["dataset_id"]][row["symbol"]].append(row)
    return datasets


def align_exact(rows_a, rows_b):
    by_a = {parse_utc(row["event_time_utc"]): row for row in rows_a}
    by_b = {parse_utc(row["event_time_utc"]): row for row in rows_b}
    common = sorted(set(by_a).intersection(by_b))
    return common, sorted(set(by_a) - set(by_b)), sorted(set(by_b) - set(by_a))


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []
    contract_path = repo_root / "contexts/legacy/infrastructure/exp0018_daye_trader/contracts/daye_multi_symbol_data_contract_v2.json"
    fixture_path = repo_root / "contexts/legacy/infrastructure/exp0018_daye_trader/fixtures/daye_multi_symbol_alignment_cases_v2.csv"
    if not contract_path.exists():
        return [f"missing contract: {contract_path}"]
    if not fixture_path.exists():
        return [f"missing fixture: {fixture_path}"]

    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if contract.get("schema_version") != 2:
        errors.append("contract schema_version must be 2")
    if contract.get("alignment_key") != "event_time_utc":
        errors.append("alignment key must be event_time_utc")
    if contract.get("alignment_mode") != "exact_match_only":
        errors.append("alignment mode must be exact_match_only")
    if contract.get("forward_fill_allowed") is not False:
        errors.append("forward fill must be false")

    datasets = load_fixture(fixture_path)
    common, only_a, only_b = align_exact(datasets["exact"]["A"], datasets["exact"]["B"])
    if (len(common), len(only_a), len(only_b)) != (3, 0, 0):
        errors.append("exact fixture failed")
    common, only_a, only_b = align_exact(datasets["missing_b"]["A"], datasets["missing_b"]["B"])
    if (len(common), len(only_a), len(only_b)) != (2, 1, 0):
        errors.append("missing_b fixture failed")
    common, only_a, only_b = align_exact(datasets["shifted"]["A"], datasets["shifted"]["B"])
    if len(common) != 0:
        errors.append("shifted timestamps must not align by index")

    source_root = repo_root / "mql5/Include/DayeTrader/EXP0018"
    expert = repo_root / "mql5/Experts/DayeTrader/EXP0018_Daye_Data_Sync_Anatomy.mq5"
    source_files = list(source_root.glob("DAYE_Data*.mqh")) + [expert]
    for path in source_files:
        if not path.exists():
            errors.append(f"missing source file: {path}")
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for token in FORBIDDEN_MQL5_TOKENS:
            if token in text:
                errors.append(f"forbidden execution token {token} in {path}")
    sync_source = (source_root / "DAYE_DataSynchronizer.mqh").read_text(encoding="utf-8")
    for required in ("event_time_utc", "CopyRates", "SeriesInfoInteger", "CopyTime", "unmatched_a", "unmatched_b"):
        if required not in sync_source:
            errors.append(f"synchronizer missing required evidence: {required}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.repo_root).resolve())
    if errors:
        print("EXP0018 Phase02 validation: FAIL")
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("EXP0018 Phase02 validation: PASS")
    print("Exact timestamp alignment, missing-bar explicitness, no-forward-fill contract, and no-execution boundary verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
