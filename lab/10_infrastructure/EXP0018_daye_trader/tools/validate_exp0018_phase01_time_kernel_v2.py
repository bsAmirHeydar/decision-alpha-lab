from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

NY = ZoneInfo("America/New_York")

@dataclass(frozen=True)
class Classified:
    ny: datetime
    offset_minutes: int
    fold: int
    trading_day_key: str
    session: str
    subcycle: str
    gap: int


def classify(utc_dt: datetime) -> Classified:
    ny = utc_dt.astimezone(NY)
    s = ny.hour * 3600 + ny.minute * 60 + ny.second
    if s >= 18*3600:
        session = "A"
    elif s < 6*3600:
        session = "L"
    elif s < 12*3600:
        session = "N"
    elif s < 17*3600:
        session = "P"
    else:
        session = "NONE"

    if s >= 18*3600:
        bounds = [(19*3600+30*60,"a1"),(21*3600,"a2"),(22*3600+30*60,"a3"),(24*3600,"a4")]
        subcycle = next(code for end, code in bounds if s < end)
    elif s < 6*3600:
        bounds = [(1*3600+30*60,"l1"),(3*3600,"l2"),(4*3600+30*60,"l3"),(6*3600,"l4")]
        subcycle = next(code for end, code in bounds if s < end)
    elif s < 12*3600:
        bounds = [(7*3600+30*60,"n1"),(9*3600,"n2"),(10*3600+30*60,"n3"),(12*3600,"n4")]
        subcycle = next(code for end, code in bounds if s < end)
    elif s < 17*3600:
        bounds = [(13*3600+30*60,"p1"),(15*3600,"p2"),(16*3600+30*60,"p3"),(17*3600,"p4")]
        subcycle = next(code for end, code in bounds if s < end)
    else:
        subcycle = "NONE"

    anchored = ny - timedelta(hours=18)
    return Classified(
        ny=ny,
        offset_minutes=int(ny.utcoffset().total_seconds()//60),
        fold=ny.fold,
        trading_day_key=anchored.strftime("%Y-%m-%d"),
        session=session,
        subcycle=subcycle,
        gap=1 if 17*3600 <= s < 18*3600 else 0,
    )


def validate(repo_root: Path) -> list[str]:
    errors: list[str] = []
    contract_path = repo_root / "lab/10_infrastructure/EXP0018_daye_trader/contracts/daye_time_contract_v2.json"
    fixtures_path = repo_root / "lab/10_infrastructure/EXP0018_daye_trader/fixtures/daye_time_golden_cases_v2.csv"
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if contract.get("execution_authority") is not False:
        errors.append("execution_authority must be false")
    if contract["subcycles"]["p4"] != ["16:30:00", "17:00:00"]:
        errors.append("p4 must remain 16:30-17:00")
    if contract["weekly"].get("enabled") is not False:
        errors.append("weekly must remain disabled until ADR-DY-A03")

    with fixtures_path.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            utc_dt = datetime.fromisoformat(row["utc_iso"].replace("Z", "+00:00"))
            got = classify(utc_dt)
            expected_ny = datetime.strptime(row["expected_ny"], "%Y-%m-%d %H:%M:%S")
            if got.ny.replace(tzinfo=None) != expected_ny:
                errors.append(f"{row['fixture_id']}: ny {got.ny} != {expected_ny}")
            checks = {
                "offset": (got.offset_minutes, int(row["expected_offset_minutes"])),
                "fold": (got.fold, int(row["expected_fold"])),
                "trading_day_key": (got.trading_day_key, row["expected_trading_day_key"]),
                "session": (got.session, row["expected_session"]),
                "subcycle": (got.subcycle, row["expected_subcycle"]),
                "gap": (got.gap, int(row["expected_gap"])),
            }
            for name, (actual, expected) in checks.items():
                if actual != expected:
                    errors.append(f"{row['fixture_id']}: {name} {actual!r} != {expected!r}")

    # Exhaustive classification: every wall-clock second maps to exactly one session/gap and one subcycle/none.
    for second in range(0, 86400):
        hour, rem = divmod(second, 3600)
        minute, sec = divmod(rem, 60)
        ny = datetime(2026, 7, 10, hour, minute, sec, tzinfo=NY)
        got = classify(ny.astimezone(timezone.utc))
        if got.gap:
            if got.session != "NONE" or got.subcycle != "NONE":
                errors.append(f"exhaustive second {second}: gap classification conflict")
                break
        else:
            if got.session == "NONE" or got.subcycle == "NONE":
                errors.append(f"exhaustive second {second}: missing active classification")
                break
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("repo_root", nargs="?", default=".")
    args = parser.parse_args()
    errors = validate(Path(args.repo_root).resolve())
    if errors:
        print("EXP0018 P01 time-kernel validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("EXP0018 P01 time-kernel validation: PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
