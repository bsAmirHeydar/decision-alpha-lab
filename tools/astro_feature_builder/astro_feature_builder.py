#!/usr/bin/env python3
"""
Decision Alpha Lab - Astro Feature Builder

Generates deterministic candle-by-candle astrological feature stores for MQL5.

Primary engine: pyswisseph / Swiss Ephemeris.
No network calls. No API dependency.

Time contract:
    broker_time = UTC + broker_gmt_offset_hours
    utc_time    = broker_time - broker_gmt_offset_hours

Every output row is aligned to a broker candle open time and contains the sky map
computed for the corresponding UTC instant.
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

EXCEL_MAX_ROWS = 1048576

try:
    import swisseph as swe
except Exception as exc:  # pragma: no cover - dependency guard for user machine
    print("ERROR: pyswisseph is not installed. Run: python -m pip install pyswisseph", file=sys.stderr)
    raise


SIGN_NAMES = [
    "aries", "taurus", "gemini", "cancer", "leo", "virgo",
    "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "pisces",
]

PLANETS: List[Tuple[str, int]] = [
    ("sun", swe.SUN),
    ("moon", swe.MOON),
    ("mercury", swe.MERCURY),
    ("venus", swe.VENUS),
    ("mars", swe.MARS),
    ("jupiter", swe.JUPITER),
    ("saturn", swe.SATURN),
    ("uranus", swe.URANUS),
    ("neptune", swe.NEPTUNE),
    ("pluto", swe.PLUTO),
    ("true_node", swe.TRUE_NODE),
    ("mean_node", swe.MEAN_NODE),
]

ASPECTS: List[Tuple[str, float]] = [
    ("conjunction", 0.0),
    ("sextile", 60.0),
    ("square", 90.0),
    ("trine", 120.0),
    ("opposition", 180.0),
]

DEFAULT_ASPECT_PAIRS = [
    ("sun", "moon"),
    ("sun", "mercury"),
    ("sun", "venus"),
    ("sun", "mars"),
    ("sun", "jupiter"),
    ("sun", "saturn"),
    ("moon", "mercury"),
    ("moon", "venus"),
    ("moon", "mars"),
    ("moon", "jupiter"),
    ("moon", "saturn"),
    ("mercury", "venus"),
    ("venus", "mars"),
    ("mars", "saturn"),
    ("jupiter", "saturn"),
]


@dataclass
class PlanetState:
    name: str
    lon: float = 0.0
    lat: float = 0.0
    dist: float = 0.0
    speed_lon: float = 0.0
    speed_lat: float = 0.0
    speed_dist: float = 0.0
    ra: float = 0.0
    decl: float = 0.0

    @property
    def sign_index(self) -> int:
        return int(math.floor(self.lon / 30.0)) % 12

    @property
    def sign_name(self) -> str:
        return SIGN_NAMES[self.sign_index]

    @property
    def degree_in_sign(self) -> float:
        return self.lon % 30.0

    @property
    def retrograde(self) -> int:
        return 1 if self.speed_lon < 0.0 else 0


@dataclass
class AspectState:
    pair: str
    angle: float
    nearest_name: str
    nearest_degree: float
    orb: float
    applying: int


@dataclass
class AstroRow:
    broker_time: datetime
    utc_time: datetime
    jd_ut: float
    planets: Dict[str, PlanetState] = field(default_factory=dict)
    aspects: Dict[str, AspectState] = field(default_factory=dict)
    moon_phase_angle: float = 0.0
    moon_phase_bucket: str = "unknown"
    moon_illumination_proxy: float = 0.0
    feature_key: str = ""
    summary: str = ""


def parse_datetime(s: str) -> datetime:
    s = s.strip().replace("T", " ")
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y.%m.%d %H:%M:%S", "%Y.%m.%d %H:%M"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            pass
    raise ValueError(f"Could not parse datetime: {s!r}")


def fmt_dt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def utc_to_jd_ut(dt_utc: datetime) -> float:
    hour = dt_utc.hour + dt_utc.minute / 60.0 + dt_utc.second / 3600.0 + dt_utc.microsecond / 3_600_000_000.0
    return swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, hour, swe.GREG_CAL)


def norm360(x: float) -> float:
    x = x % 360.0
    if x < 0.0:
        x += 360.0
    return x


def angular_distance_180(a: float, b: float) -> float:
    d = abs(norm360(a - b))
    return min(d, 360.0 - d)


def nearest_aspect(angle: float) -> Tuple[str, float, float]:
    best_name = "none"
    best_degree = -1.0
    best_orb = 999.0
    for name, deg in ASPECTS:
        orb = abs(angle - deg)
        if orb < best_orb:
            best_name = name
            best_degree = deg
            best_orb = orb
    return best_name, best_degree, best_orb


def moon_phase_bucket(angle: float) -> str:
    # angle is Moon - Sun, normalized 0..360
    bins = [
        (22.5, "new"),
        (67.5, "waxing_crescent"),
        (112.5, "first_quarter"),
        (157.5, "waxing_gibbous"),
        (202.5, "full"),
        (247.5, "waning_gibbous"),
        (292.5, "last_quarter"),
        (337.5, "waning_crescent"),
        (360.0, "new"),
    ]
    for bound, name in bins:
        if angle < bound:
            return name
    return "new"


def calc_planet(jd_ut: float, name: str, planet_id: int, flags: int) -> PlanetState:
    xx, ret = swe.calc_ut(jd_ut, planet_id, flags)
    lon, lat, dist, speed_lon, speed_lat, speed_dist = xx[:6]

    # Equatorial call for RA/declination. Keep it separate so ecliptic lon/lat remain canonical.
    eq_flags = flags | swe.FLG_EQUATORIAL
    eq, _ = swe.calc_ut(jd_ut, planet_id, eq_flags)
    ra, decl = eq[0], eq[1]

    return PlanetState(
        name=name,
        lon=norm360(lon),
        lat=lat,
        dist=dist,
        speed_lon=speed_lon,
        speed_lat=speed_lat,
        speed_dist=speed_dist,
        ra=ra,
        decl=decl,
    )


def calc_aspect(a: PlanetState, b: PlanetState, delta_days: float = 1.0 / 1440.0) -> AspectState:
    angle_now = angular_distance_180(a.lon, b.lon)
    nearest_name, nearest_degree, orb_now = nearest_aspect(angle_now)

    a_next = norm360(a.lon + a.speed_lon * delta_days)
    b_next = norm360(b.lon + b.speed_lon * delta_days)
    angle_next = angular_distance_180(a_next, b_next)
    _, _, orb_next = nearest_aspect(angle_next)
    applying = 1 if orb_next < orb_now else 0

    pair = f"{a.name}_{b.name}"
    return AspectState(pair, angle_now, nearest_name, nearest_degree, orb_now, applying)


def quantile(values: Sequence[float], q: float) -> float:
    if not values:
        return 0.0
    xs = sorted(values)
    idx = (len(xs) - 1) * q
    lo = int(math.floor(idx))
    hi = int(math.ceil(idx))
    if lo == hi:
        return xs[lo]
    return xs[lo] * (hi - idx) + xs[hi] * (idx - lo)


def bucket3(x: float, q1: float, q2: float) -> str:
    if x <= q1:
        return "low"
    if x <= q2:
        return "mid"
    return "high"


def build_feature_key(row: AstroRow, speed_buckets: Dict[str, str], aspect_orb_limit: float) -> str:
    parts: List[str] = []
    parts.append(f"moon_phase={row.moon_phase_bucket}")

    for p in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
        st = row.planets[p]
        parts.append(f"{p}_sign={st.sign_name}")
        parts.append(f"{p}_retro={st.retrograde}")
        parts.append(f"{p}_speed={speed_buckets.get(p, 'na')}")

    for pair_key in ("sun_moon", "mars_saturn", "venus_mars", "jupiter_saturn"):
        asp = row.aspects.get(pair_key)
        if asp is None:
            continue
        if asp.orb <= aspect_orb_limit:
            parts.append(f"{pair_key}_asp={asp.nearest_name}")
            parts.append(f"{pair_key}_app={asp.applying}")
        else:
            parts.append(f"{pair_key}_asp=none")

    return "|".join(parts)


def build_summary(row: AstroRow) -> str:
    sun = row.planets["sun"]
    moon = row.planets["moon"]
    mars = row.planets["mars"]
    saturn = row.planets["saturn"]
    ms = row.aspects.get("mars_saturn")
    ms_text = "none"
    if ms is not None:
        ms_text = f"{ms.nearest_name}:{ms.orb:.2f}:{'app' if ms.applying else 'sep'}"
    return (
        f"moon_phase={row.moon_phase_bucket};"
        f"sun={sun.sign_name}:{sun.degree_in_sign:.2f};"
        f"moon={moon.sign_name}:{moon.degree_in_sign:.2f};"
        f"mars={mars.sign_name}:{mars.degree_in_sign:.2f};"
        f"saturn={saturn.sign_name}:{saturn.degree_in_sign:.2f};"
        f"mars_saturn={ms_text}"
    )


def generate_rows(
    start_broker: datetime,
    end_broker: datetime,
    timeframe_minutes: int,
    broker_gmt_offset_hours: float,
    aspect_orb_limit: float,
) -> List[AstroRow]:
    if timeframe_minutes <= 0:
        raise ValueError("timeframe_minutes must be positive")
    if end_broker <= start_broker:
        raise ValueError("end_broker must be after start_broker")

    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    offset = timedelta(hours=broker_gmt_offset_hours)
    step = timedelta(minutes=timeframe_minutes)
    rows: List[AstroRow] = []

    t_broker = start_broker
    while t_broker < end_broker:
        t_utc = t_broker - offset
        t_utc = t_utc.replace(tzinfo=None)
        jd = utc_to_jd_ut(t_utc)

        row = AstroRow(broker_time=t_broker, utc_time=t_utc, jd_ut=jd)
        for name, pid in PLANETS:
            row.planets[name] = calc_planet(jd, name, pid, flags)

        for a_name, b_name in DEFAULT_ASPECT_PAIRS:
            row.aspects[f"{a_name}_{b_name}"] = calc_aspect(row.planets[a_name], row.planets[b_name])

        row.moon_phase_angle = norm360(row.planets["moon"].lon - row.planets["sun"].lon)
        row.moon_phase_bucket = moon_phase_bucket(row.moon_phase_angle)
        row.moon_illumination_proxy = (1.0 - math.cos(math.radians(row.moon_phase_angle))) / 2.0
        rows.append(row)
        t_broker += step

    # Mark ingress by looking at previous row and compute speed quantile buckets.
    speed_values: Dict[str, List[float]] = {p: [] for p, _ in PLANETS}
    for row in rows:
        for p, _ in PLANETS:
            speed_values[p].append(abs(row.planets[p].speed_lon))

    speed_q: Dict[str, Tuple[float, float]] = {}
    for p, values in speed_values.items():
        speed_q[p] = (quantile(values, 0.33), quantile(values, 0.66))

    for row in rows:
        sb: Dict[str, str] = {}
        for p, _ in PLANETS:
            q1, q2 = speed_q[p]
            sb[p] = bucket3(abs(row.planets[p].speed_lon), q1, q2)
        row.feature_key = build_feature_key(row, sb, aspect_orb_limit)
        row.summary = build_summary(row)

    return rows


def make_headers() -> List[str]:
    headers = [
        "broker_time",
        "utc_time",
        "unix_utc",
        "jd_ut",
        "feature_key",
        "summary",
        "moon_phase_angle",
        "moon_phase_bucket",
        "moon_illumination_proxy",
    ]
    for p, _ in PLANETS:
        headers += [
            f"{p}_lon",
            f"{p}_lat",
            f"{p}_dist",
            f"{p}_speed_lon",
            f"{p}_speed_lat",
            f"{p}_speed_dist",
            f"{p}_ra",
            f"{p}_decl",
            f"{p}_sign",
            f"{p}_sign_index",
            f"{p}_degree",
            f"{p}_retro",
        ]
    for a, b in DEFAULT_ASPECT_PAIRS:
        key = f"{a}_{b}"
        headers += [
            f"{key}_angle",
            f"{key}_aspect",
            f"{key}_orb",
            f"{key}_applying",
        ]
    return headers


def row_to_dict(row: AstroRow) -> Dict[str, object]:
    d: Dict[str, object] = {
        "broker_time": fmt_dt(row.broker_time),
        "utc_time": fmt_dt(row.utc_time),
        "unix_utc": int(row.utc_time.replace(tzinfo=timezone.utc).timestamp()),
        "jd_ut": f"{row.jd_ut:.9f}",
        "feature_key": row.feature_key,
        "summary": row.summary,
        "moon_phase_angle": f"{row.moon_phase_angle:.8f}",
        "moon_phase_bucket": row.moon_phase_bucket,
        "moon_illumination_proxy": f"{row.moon_illumination_proxy:.8f}",
    }
    for p, _ in PLANETS:
        st = row.planets[p]
        d.update({
            f"{p}_lon": f"{st.lon:.8f}",
            f"{p}_lat": f"{st.lat:.8f}",
            f"{p}_dist": f"{st.dist:.10f}",
            f"{p}_speed_lon": f"{st.speed_lon:.10f}",
            f"{p}_speed_lat": f"{st.speed_lat:.10f}",
            f"{p}_speed_dist": f"{st.speed_dist:.10f}",
            f"{p}_ra": f"{st.ra:.8f}",
            f"{p}_decl": f"{st.decl:.8f}",
            f"{p}_sign": st.sign_name,
            f"{p}_sign_index": st.sign_index,
            f"{p}_degree": f"{st.degree_in_sign:.8f}",
            f"{p}_retro": st.retrograde,
        })
    for a, b in DEFAULT_ASPECT_PAIRS:
        key = f"{a}_{b}"
        asp = row.aspects[key]
        d.update({
            f"{key}_angle": f"{asp.angle:.8f}",
            f"{key}_aspect": asp.nearest_name,
            f"{key}_orb": f"{asp.orb:.8f}",
            f"{key}_applying": asp.applying,
        })
    return d


def write_csv(rows: Sequence[AstroRow], out_path: str) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    headers = make_headers()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row_to_dict(row))


def write_xlsx(rows: Sequence[AstroRow], out_path: str, broker_gmt_offset_hours: float, timeframe_minutes: int) -> None:
    """Write a human-inspection Excel workbook.

    MQL5 should read the CSV mirror, not the .xlsx binary file.
    Excel has a hard worksheet row limit, so large M1 ranges should be split
    into month/year chunks.
    """
    if len(rows) + 1 > EXCEL_MAX_ROWS:
        raise ValueError(
            f"Excel worksheet row limit exceeded: rows={len(rows)}. "
            f"Split the date range into smaller chunks or use CSV only."
        )

    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, PatternFill, Alignment
        from openpyxl.utils import get_column_letter
    except Exception as exc:  # pragma: no cover - user machine dependency guard
        raise RuntimeError(
            "openpyxl is required for --out-xlsx. Run: python -m pip install openpyxl"
        ) from exc

    os.makedirs(os.path.dirname(os.path.abspath(out_path)) or ".", exist_ok=True)
    headers = make_headers()
    wb = Workbook()
    ws = wb.active
    ws.title = "astro_rows"
    ws.freeze_panes = "A2"

    ws.append(headers)
    for row in rows:
        d = row_to_dict(row)
        ws.append([d.get(h, "") for h in headers])

    header_fill = PatternFill("solid", fgColor="1F4E78")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")

    # Widths are bounded so the workbook remains usable even with many columns.
    for idx, header in enumerate(headers, start=1):
        width = 12
        if header in ("broker_time", "utc_time"):
            width = 20
        elif header in ("feature_key", "summary"):
            width = 45
        elif header.endswith("_aspect") or header.endswith("_sign") or header.endswith("_bucket"):
            width = 16
        ws.column_dimensions[get_column_letter(idx)].width = width

    ws_meta = wb.create_sheet("meta")
    meta_rows = [
        ["field", "value"],
        ["rows", len(rows)],
        ["timeframe_minutes", timeframe_minutes],
        ["broker_gmt_offset_hours", broker_gmt_offset_hours],
        ["time_contract", "utc_time = broker_time - broker_gmt_offset_hours"],
        ["mql_runtime_file", "Use the CSV mirror in MQL5/Files, not this .xlsx file"],
        ["causality", "Each row is computed for candle open time only; no future market information is used"],
    ]
    for r in meta_rows:
        ws_meta.append(r)
    ws_meta.column_dimensions["A"].width = 28
    ws_meta.column_dimensions["B"].width = 80
    for cell in ws_meta[1]:
        cell.fill = header_fill
        cell.font = header_font

    ws_dict = wb.create_sheet("feature_dictionary")
    dict_rows = [
        ["feature_family", "raw_columns", "derived_feature", "research meaning"],
        ["longitude", "*_lon", "sign / degree / aspect geometry", "cyclical angular location; used only as a distributional time-state"],
        ["speed", "*_speed_lon", "retrograde / station / speed bucket", "momentum state of the planetary cycle; useful for regime bucketing"],
        ["declination", "*_decl", "north/south/out_of_bounds/parallels", "vertical sky position; tested as a separate distributional axis"],
        ["moon phase", "moon_phase_angle", "phase bucket / illumination proxy", "lunar cycle state; tested for volatility/path distribution shifts"],
        ["aspects", "*_angle/*_orb/*_applying", "aspect class + orb tightness + applying", "pairwise angular relationship; no causal claim, only conditional distribution test"],
    ]
    for r in dict_rows:
        ws_dict.append(r)
    for cell in ws_dict[1]:
        cell.fill = header_fill
        cell.font = header_font
    ws_dict.column_dimensions["A"].width = 20
    ws_dict.column_dimensions["B"].width = 28
    ws_dict.column_dimensions["C"].width = 34
    ws_dict.column_dimensions["D"].width = 80

    wb.save(out_path)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Build candle-aligned astro feature CSV/XLSX for MQL5")
    parser.add_argument("--start-broker", required=True, help="Broker start time, e.g. 2024-01-01 00:00:00")
    parser.add_argument("--end-broker", required=True, help="Broker end time, exclusive")
    parser.add_argument("--timeframe-minutes", type=int, default=1, help="Candle interval in minutes")
    parser.add_argument("--broker-gmt-offset-hours", type=float, required=True, help="Broker time offset from UTC. Example UTC+2 => 2")
    parser.add_argument("--ephe-path", default="", help="Swiss Ephemeris file directory. Optional if package defaults are enough.")
    parser.add_argument("--out", default="", help="Backward-compatible output CSV path. Prefer --out-csv.")
    parser.add_argument("--out-csv", default="", help="Output CSV path for MQL5 runtime reading")
    parser.add_argument("--out-xlsx", default="", help="Optional Excel .xlsx path for human inspection")
    parser.add_argument("--aspect-orb-limit", type=float, default=6.0, help="Aspect orb limit used inside feature_key")
    args = parser.parse_args(argv)

    if args.ephe_path:
        swe.set_ephe_path(args.ephe_path)

    start = parse_datetime(args.start_broker)
    end = parse_datetime(args.end_broker)
    rows = generate_rows(
        start_broker=start,
        end_broker=end,
        timeframe_minutes=args.timeframe_minutes,
        broker_gmt_offset_hours=args.broker_gmt_offset_hours,
        aspect_orb_limit=args.aspect_orb_limit,
    )
    out_csv = args.out_csv or args.out
    if not out_csv and not args.out_xlsx:
        raise ValueError("Provide --out-csv and/or --out-xlsx")

    if out_csv:
        write_csv(rows, out_csv)
        print(f"Wrote {len(rows)} astro feature CSV rows to {out_csv}")

    if args.out_xlsx:
        write_xlsx(rows, args.out_xlsx, args.broker_gmt_offset_hours, args.timeframe_minutes)
        print(f"Wrote {len(rows)} astro feature Excel rows to {args.out_xlsx}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
