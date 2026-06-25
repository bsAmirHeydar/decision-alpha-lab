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

CORE_BODIES: List[str] = [
    "sun",
    "moon",
    "mercury",
    "venus",
    "mars",
    "jupiter",
    "saturn",
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
    house: int = -1

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
    houses_valid: bool = False
    house_lat: float = 0.0
    house_lon: float = 0.0
    house_system: str = ""
    asc_lon: float = 0.0
    mc_lon: float = 0.0
    house_cusps: List[float] = field(default_factory=list)
    natal_enabled: bool = False
    natal_label: str = ""
    natal_local_time: Optional[datetime] = None
    natal_utc_time: Optional[datetime] = None
    natal_utc_offset_hours: float = 0.0
    natal_houses_valid: bool = False
    natal_house_lat: float = 0.0
    natal_house_lon: float = 0.0
    natal_house_system: str = ""
    natal_asc_lon: float = 0.0
    natal_mc_lon: float = 0.0
    natal_house_cusps: List[float] = field(default_factory=list)
    natal_planets: Dict[str, PlanetState] = field(default_factory=dict)
    transit_natal_aspects: Dict[str, AspectState] = field(default_factory=dict)
    transit_in_natal_houses: Dict[str, int] = field(default_factory=dict)
    feature_key: str = ""
    summary: str = ""
    astro_bias_text: str = ""
    astro_path_text: str = ""
    astro_signal_text: str = ""


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




def longitude_in_arc(lon: float, start: float, end: float) -> bool:
    lon = norm360(lon)
    start = norm360(start)
    end = norm360(end)
    if start <= end:
        return start <= lon < end
    return lon >= start or lon < end


def house_for_longitude(lon: float, cusps: Sequence[float]) -> int:
    if len(cusps) < 12:
        return -1
    for i in range(12):
        start = cusps[i]
        end = cusps[(i + 1) % 12]
        if longitude_in_arc(lon, start, end):
            return i + 1
    return -1


def calc_houses(jd_ut: float, lat: Optional[float], lon: Optional[float], system: str) -> Tuple[bool, List[float], float, float]:
    if lat is None or lon is None:
        return False, [0.0] * 12, 0.0, 0.0
    if not (-90.0 <= lat <= 90.0):
        raise ValueError(f"house latitude out of range: {lat}")
    if not (-180.0 <= lon <= 180.0):
        raise ValueError(f"house longitude out of range: {lon}")
    hsys = (system or "P").strip()[:1] or "P"
    try:
        cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys.encode("ascii"))
    except TypeError:
        cusps, ascmc = swe.houses_ex(jd_ut, lat, lon, hsys)
    cusps12 = [norm360(float(x)) for x in list(cusps)[:12]]
    asc = norm360(float(ascmc[0])) if len(ascmc) > 0 else 0.0
    mc = norm360(float(ascmc[1])) if len(ascmc) > 1 else 0.0
    return True, cusps12, asc, mc

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


def calc_named_aspect(a_name: str, a: PlanetState, b_name: str, b: PlanetState, delta_days: float = 1.0 / 1440.0) -> AspectState:
    asp = calc_aspect(a, b, delta_days)
    asp.pair = f"t_{a_name}__n_{b_name}"
    return asp


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


def compute_chart(
    jd_ut: float,
    *,
    house_lat: Optional[float],
    house_lon: Optional[float],
    house_system: str,
) -> Tuple[Dict[str, PlanetState], bool, List[float], float, float]:
    flags = swe.FLG_SWIEPH | swe.FLG_SPEED
    planets: Dict[str, PlanetState] = {}
    for name, pid in PLANETS:
        planets[name] = calc_planet(jd_ut, name, pid, flags)

    houses_valid, house_cusps, asc_lon, mc_lon = calc_houses(jd_ut, house_lat, house_lon, house_system)
    if houses_valid:
        for st in planets.values():
            st.house = house_for_longitude(st.lon, house_cusps)

    return planets, houses_valid, house_cusps, asc_lon, mc_lon


def astro_language_bias(row: AstroRow) -> str:
    fire = 0
    air = 0
    earth = 0
    water = 0
    cardinal = 0
    fixed = 0
    mutable = 0
    for name in CORE_BODIES:
        sign = row.planets[name].sign_name
        if sign in ("aries", "leo", "sagittarius"):
            fire += 1
        elif sign in ("gemini", "libra", "aquarius"):
            air += 1
        elif sign in ("taurus", "virgo", "capricorn"):
            earth += 1
        else:
            water += 1

        if sign in ("aries", "cancer", "libra", "capricorn"):
            cardinal += 1
        elif sign in ("taurus", "leo", "scorpio", "aquarius"):
            fixed += 1
        else:
            mutable += 1

    impulse = fire + air
    compression = earth + water
    if impulse >= compression + 2 and cardinal >= max(fixed, mutable):
        return "impulsive_cardinal_bias"
    if earth >= 3 and fixed >= max(cardinal, mutable):
        return "fixed_earth_bias"
    if water >= 3:
        return "water_reactive_bias"
    if air >= 3:
        return "air_distributive_bias"
    return "mixed_bias"


def astro_language_path(row: AstroRow) -> str:
    ms = row.aspects.get("mars_saturn")
    sm = row.aspects.get("sun_moon")
    js = row.aspects.get("jupiter_saturn")
    pressure = 0
    flow = 0
    transition = 0

    for asp in (ms, sm, js):
        if asp is None or asp.orb > 6.0:
            continue
        if asp.nearest_name in ("square", "opposition"):
            pressure += 2
        elif asp.nearest_name == "conjunction":
            pressure += 1
        elif asp.nearest_name in ("trine", "sextile"):
            flow += 2
        if asp.applying == 1 and asp.orb <= 2.0:
            transition += 1

    moon_deg = row.planets["moon"].degree_in_sign
    if moon_deg <= 1.0 or moon_deg >= 29.0:
        transition += 2
    if abs(row.planets["mercury"].speed_lon) <= 0.08 or abs(row.planets["mars"].speed_lon) <= 0.025:
        transition += 2

    if pressure >= flow + 2:
        return "frictional_path"
    if flow >= pressure + 2 and transition <= 1:
        return "clean_flow_path"
    if transition >= 3:
        return "threshold_transition_path"
    return "mixed_path"


def astro_language_signal(row: AstroRow) -> str:
    bias = astro_language_bias(row)
    path = astro_language_path(row)
    moon_phase = row.moon_phase_bucket

    if bias in ("impulsive_cardinal_bias", "air_distributive_bias") and path in ("clean_flow_path", "mixed_path") and "waxing" in moon_phase:
        return "astro_long_permission"
    if bias in ("fixed_earth_bias", "water_reactive_bias") and path == "frictional_path" and ("waning" in moon_phase or moon_phase == "full"):
        return "astro_short_permission"
    if path == "threshold_transition_path":
        return "astro_wait_transition"
    return "astro_neutral_permission"


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

    if row.natal_enabled:
        parts.append(f"natal_label={row.natal_label or 'natal'}")
        for pair_key in ("t_sun__n_sun", "t_moon__n_moon", "t_mars__n_saturn", "t_jupiter__n_mars"):
            asp = row.transit_natal_aspects.get(pair_key)
            if asp is None:
                continue
            if asp.orb <= aspect_orb_limit:
                parts.append(f"{pair_key}_asp={asp.nearest_name}")
                parts.append(f"{pair_key}_app={asp.applying}")
            else:
                parts.append(f"{pair_key}_asp=none")

    parts.append(f"astro_bias={row.astro_bias_text or astro_language_bias(row)}")
    parts.append(f"astro_path={row.astro_path_text or astro_language_path(row)}")
    parts.append(f"astro_signal={row.astro_signal_text or astro_language_signal(row)}")

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
        f"mars_saturn={ms_text};"
        f"bias={row.astro_bias_text or astro_language_bias(row)};"
        f"path={row.astro_path_text or astro_language_path(row)};"
        f"signal={row.astro_signal_text or astro_language_signal(row)}"
    )


def generate_rows(
    start_broker: datetime,
    end_broker: datetime,
    timeframe_minutes: int,
    broker_gmt_offset_hours: float,
    aspect_orb_limit: float,
    house_lat: Optional[float] = None,
    house_lon: Optional[float] = None,
    house_system: str = "P",
    natal_local_dt: Optional[datetime] = None,
    natal_utc_offset_hours: float = 0.0,
    natal_lat: Optional[float] = None,
    natal_lon: Optional[float] = None,
    natal_house_system: str = "P",
    natal_label: str = "",
) -> List[AstroRow]:
    if timeframe_minutes <= 0:
        raise ValueError("timeframe_minutes must be positive")
    if end_broker <= start_broker:
        raise ValueError("end_broker must be after start_broker")

    offset = timedelta(hours=broker_gmt_offset_hours)
    step = timedelta(minutes=timeframe_minutes)
    rows: List[AstroRow] = []
    natal_planets: Dict[str, PlanetState] = {}
    natal_houses_valid = False
    natal_house_cusps: List[float] = [0.0] * 12
    natal_asc_lon = 0.0
    natal_mc_lon = 0.0
    natal_utc_time: Optional[datetime] = None
    natal_enabled = natal_local_dt is not None

    if natal_enabled:
        natal_utc_time = natal_local_dt - timedelta(hours=natal_utc_offset_hours)
        natal_jd = utc_to_jd_ut(natal_utc_time)
        natal_planets, natal_houses_valid, natal_house_cusps, natal_asc_lon, natal_mc_lon = compute_chart(
            natal_jd,
            house_lat=natal_lat,
            house_lon=natal_lon,
            house_system=natal_house_system,
        )

    t_broker = start_broker
    while t_broker < end_broker:
        t_utc = t_broker - offset
        t_utc = t_utc.replace(tzinfo=None)
        jd = utc_to_jd_ut(t_utc)

        row = AstroRow(broker_time=t_broker, utc_time=t_utc, jd_ut=jd)
        row.planets, houses_valid, house_cusps, asc_lon, mc_lon = compute_chart(
            jd,
            house_lat=house_lat,
            house_lon=house_lon,
            house_system=house_system,
        )
        row.houses_valid = houses_valid
        row.house_lat = house_lat if house_lat is not None else 0.0
        row.house_lon = house_lon if house_lon is not None else 0.0
        row.house_system = (house_system or "P").strip()[:1] if houses_valid else ""
        row.house_cusps = house_cusps
        row.asc_lon = asc_lon
        row.mc_lon = mc_lon

        for a_name, b_name in DEFAULT_ASPECT_PAIRS:
            row.aspects[f"{a_name}_{b_name}"] = calc_aspect(row.planets[a_name], row.planets[b_name])

        row.moon_phase_angle = norm360(row.planets["moon"].lon - row.planets["sun"].lon)
        row.moon_phase_bucket = moon_phase_bucket(row.moon_phase_angle)
        row.moon_illumination_proxy = (1.0 - math.cos(math.radians(row.moon_phase_angle))) / 2.0

        if natal_enabled:
            row.natal_enabled = True
            row.natal_label = natal_label or "natal"
            row.natal_local_time = natal_local_dt
            row.natal_utc_time = natal_utc_time
            row.natal_utc_offset_hours = natal_utc_offset_hours
            row.natal_houses_valid = natal_houses_valid
            row.natal_house_lat = natal_lat if natal_lat is not None else 0.0
            row.natal_house_lon = natal_lon if natal_lon is not None else 0.0
            row.natal_house_system = natal_house_system if natal_houses_valid else ""
            row.natal_asc_lon = natal_asc_lon
            row.natal_mc_lon = natal_mc_lon
            row.natal_house_cusps = list(natal_house_cusps)
            row.natal_planets = {name: PlanetState(**vars(st)) for name, st in natal_planets.items()}

            for t_name in CORE_BODIES:
                if natal_houses_valid:
                    row.transit_in_natal_houses[t_name] = house_for_longitude(row.planets[t_name].lon, natal_house_cusps)
                else:
                    row.transit_in_natal_houses[t_name] = -1
                for n_name in CORE_BODIES:
                    key = f"t_{t_name}__n_{n_name}"
                    row.transit_natal_aspects[key] = calc_named_aspect(
                        t_name,
                        row.planets[t_name],
                        n_name,
                        row.natal_planets[n_name],
                    )

        row.astro_bias_text = astro_language_bias(row)
        row.astro_path_text = astro_language_path(row)
        row.astro_signal_text = astro_language_signal(row)
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
        "houses_valid",
        "house_lat",
        "house_lon",
        "house_system",
        "asc_lon",
        "mc_lon",
        "natal_enabled",
        "natal_label",
        "natal_local_time",
        "natal_utc_time",
        "natal_utc_offset_hours",
        "natal_houses_valid",
        "natal_house_lat",
        "natal_house_lon",
        "natal_house_system",
        "natal_asc_lon",
        "natal_mc_lon",
        "astro_bias_text",
        "astro_path_text",
        "astro_signal_text",
    ]
    for h in range(1, 13):
        headers.append(f"house_{h}_cusp")
    for h in range(1, 13):
        headers.append(f"natal_house_{h}_cusp")
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
            f"{p}_house",
        ]
    for p, _ in PLANETS:
        headers += [
            f"natal_{p}_lon",
            f"natal_{p}_lat",
            f"natal_{p}_dist",
            f"natal_{p}_speed_lon",
            f"natal_{p}_speed_lat",
            f"natal_{p}_speed_dist",
            f"natal_{p}_ra",
            f"natal_{p}_decl",
            f"natal_{p}_sign",
            f"natal_{p}_sign_index",
            f"natal_{p}_degree",
            f"natal_{p}_retro",
            f"natal_{p}_house",
        ]
    for a, b in DEFAULT_ASPECT_PAIRS:
        key = f"{a}_{b}"
        headers += [
            f"{key}_angle",
            f"{key}_aspect",
            f"{key}_orb",
            f"{key}_applying",
        ]
    for t_name in CORE_BODIES:
        headers.append(f"{t_name}_in_natal_house")
        for n_name in CORE_BODIES:
            key = f"t_{t_name}__n_{n_name}"
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
        "houses_valid": 1 if row.houses_valid else 0,
        "house_lat": f"{row.house_lat:.8f}",
        "house_lon": f"{row.house_lon:.8f}",
        "house_system": row.house_system,
        "asc_lon": f"{row.asc_lon:.8f}",
        "mc_lon": f"{row.mc_lon:.8f}",
        "natal_enabled": 1 if row.natal_enabled else 0,
        "natal_label": row.natal_label,
        "natal_local_time": fmt_dt(row.natal_local_time) if row.natal_local_time else "",
        "natal_utc_time": fmt_dt(row.natal_utc_time) if row.natal_utc_time else "",
        "natal_utc_offset_hours": f"{row.natal_utc_offset_hours:.4f}",
        "natal_houses_valid": 1 if row.natal_houses_valid else 0,
        "natal_house_lat": f"{row.natal_house_lat:.8f}",
        "natal_house_lon": f"{row.natal_house_lon:.8f}",
        "natal_house_system": row.natal_house_system,
        "natal_asc_lon": f"{row.natal_asc_lon:.8f}",
        "natal_mc_lon": f"{row.natal_mc_lon:.8f}",
        "astro_bias_text": row.astro_bias_text,
        "astro_path_text": row.astro_path_text,
        "astro_signal_text": row.astro_signal_text,
    }
    cusps = row.house_cusps if row.house_cusps else [0.0] * 12
    for h in range(1, 13):
        d[f"house_{h}_cusp"] = f"{cusps[h - 1]:.8f}"
    natal_cusps = row.natal_house_cusps if row.natal_house_cusps else [0.0] * 12
    for h in range(1, 13):
        d[f"natal_house_{h}_cusp"] = f"{natal_cusps[h - 1]:.8f}"
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
            f"{p}_house": st.house,
        })
    for p, _ in PLANETS:
        st = row.natal_planets.get(p)
        if st is None or not row.natal_enabled:
            st = PlanetState(name=p)
        d.update({
            f"natal_{p}_lon": f"{st.lon:.8f}",
            f"natal_{p}_lat": f"{st.lat:.8f}",
            f"natal_{p}_dist": f"{st.dist:.10f}",
            f"natal_{p}_speed_lon": f"{st.speed_lon:.10f}",
            f"natal_{p}_speed_lat": f"{st.speed_lat:.10f}",
            f"natal_{p}_speed_dist": f"{st.speed_dist:.10f}",
            f"natal_{p}_ra": f"{st.ra:.8f}",
            f"natal_{p}_decl": f"{st.decl:.8f}",
            f"natal_{p}_sign": st.sign_name if row.natal_enabled else "",
            f"natal_{p}_sign_index": st.sign_index if row.natal_enabled else -1,
            f"natal_{p}_degree": f"{st.degree_in_sign:.8f}" if row.natal_enabled else "",
            f"natal_{p}_retro": st.retrograde if row.natal_enabled else 0,
            f"natal_{p}_house": st.house if row.natal_enabled else -1,
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
    for t_name in CORE_BODIES:
        d[f"{t_name}_in_natal_house"] = row.transit_in_natal_houses.get(t_name, -1)
        for n_name in CORE_BODIES:
            key = f"t_{t_name}__n_{n_name}"
            asp = row.transit_natal_aspects.get(key)
            if asp is None:
                asp = AspectState(key, 0.0, "none", -1.0, 999.0, 0)
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
    parser.add_argument("--house-lat", type=float, default=None, help="Optional latitude for house cusps. If omitted, houses are disabled.")
    parser.add_argument("--house-lon", type=float, default=None, help="Optional longitude for house cusps. If omitted, houses are disabled.")
    parser.add_argument("--house-system", default="P", help="Swiss Ephemeris house system code. Default P=Placidus.")
    parser.add_argument("--natal-local-datetime", default="", help="Optional natal/inception local datetime, e.g. 1987-08-16 14:35:00")
    parser.add_argument("--natal-utc-offset-hours", type=float, default=0.0, help="UTC offset used to convert natal local time to UTC.")
    parser.add_argument("--natal-lat", type=float, default=None, help="Optional natal latitude.")
    parser.add_argument("--natal-lon", type=float, default=None, help="Optional natal longitude.")
    parser.add_argument("--natal-house-system", default="P", help="Natal house system code. Default P=Placidus.")
    parser.add_argument("--natal-label", default="", help="Optional natal chart label written into the CSV.")
    args = parser.parse_args(argv)

    if args.ephe_path:
        swe.set_ephe_path(args.ephe_path)

    if (args.house_lat is None) != (args.house_lon is None):
        raise ValueError("Provide both --house-lat and --house-lon, or omit both to disable houses")
    natal_dt = parse_datetime(args.natal_local_datetime) if args.natal_local_datetime else None
    if natal_dt is not None and ((args.natal_lat is None) != (args.natal_lon is None)):
        raise ValueError("Provide both --natal-lat and --natal-lon, or omit both for a houseless natal chart")

    start = parse_datetime(args.start_broker)
    end = parse_datetime(args.end_broker)
    rows = generate_rows(
        start_broker=start,
        end_broker=end,
        timeframe_minutes=args.timeframe_minutes,
        broker_gmt_offset_hours=args.broker_gmt_offset_hours,
        aspect_orb_limit=args.aspect_orb_limit,
        house_lat=args.house_lat,
        house_lon=args.house_lon,
        house_system=args.house_system,
        natal_local_dt=natal_dt,
        natal_utc_offset_hours=args.natal_utc_offset_hours,
        natal_lat=args.natal_lat,
        natal_lon=args.natal_lon,
        natal_house_system=args.natal_house_system,
        natal_label=args.natal_label,
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
