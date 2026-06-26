#!/usr/bin/env python3
"""
Run astro-only paper execution families directly on deterministic feature CSV files.

This runner is research-side infrastructure for EXP0013:
- reads raw astro feature CSVs produced by astro_feature_builder.py
- computes a pure astrology timing stack from raw astro state
- applies family-specific entry/exit doctrine
- simulates the astro execution state machine
- writes a journal with the same schema used by the MQL paper executors
"""

from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional


HOUSE_ANGULARITY = {
    1: 100.0, 10: 100.0, 7: 100.0, 4: 100.0,
    2: 62.0, 11: 62.0, 8: 62.0, 5: 62.0,
    3: 32.0, 12: 32.0, 9: 32.0, 6: 32.0,
}

SIGN_ELEMENT = {
    "aries": "fire", "leo": "fire", "sagittarius": "fire",
    "gemini": "air", "libra": "air", "aquarius": "air",
    "taurus": "earth", "virgo": "earth", "capricorn": "earth",
    "cancer": "water", "scorpio": "water", "pisces": "water",
}

SIGN_MODALITY = {
    "aries": "cardinal", "cancer": "cardinal", "libra": "cardinal", "capricorn": "cardinal",
    "taurus": "fixed", "leo": "fixed", "scorpio": "fixed", "aquarius": "fixed",
    "gemini": "mutable", "virgo": "mutable", "sagittarius": "mutable", "pisces": "mutable",
}

SOFT_ASPECTS = {"trine", "sextile"}
HARD_ASPECTS = {"square", "opposition"}

FAMILY_DEFAULTS = {
    "A0001": {
        "family_name": "A0001_transit_trend_pulse",
        "arm_threshold": 58.0,
        "enter_threshold": 66.0,
        "reduce_threshold": 52.0,
        "exit_threshold": 58.0,
        "natal_activation_minimum": 40.0,
        "friction_minimum": 60.0,
        "benefic_support_minimum": 62.0,
        "malefic_pressure_minimum": 60.0,
        "house_edge_minimum": 8.0,
    },
    "A0002": {
        "family_name": "A0002_natal_resonance",
        "arm_threshold": 60.0,
        "enter_threshold": 67.0,
        "reduce_threshold": 54.0,
        "exit_threshold": 59.0,
        "natal_activation_minimum": 46.0,
        "friction_minimum": 60.0,
        "benefic_support_minimum": 62.0,
        "malefic_pressure_minimum": 60.0,
        "house_edge_minimum": 8.0,
    },
    "A0003": {
        "family_name": "A0003_friction_polarity",
        "arm_threshold": 57.0,
        "enter_threshold": 65.0,
        "reduce_threshold": 50.0,
        "exit_threshold": 57.0,
        "natal_activation_minimum": 40.0,
        "friction_minimum": 58.0,
        "benefic_support_minimum": 62.0,
        "malefic_pressure_minimum": 60.0,
        "house_edge_minimum": 8.0,
    },
    "A0004": {
        "family_name": "A0004_sect_benefic_pressure",
        "arm_threshold": 59.0,
        "enter_threshold": 67.0,
        "reduce_threshold": 53.0,
        "exit_threshold": 59.0,
        "natal_activation_minimum": 40.0,
        "friction_minimum": 60.0,
        "benefic_support_minimum": 64.0,
        "malefic_pressure_minimum": 62.0,
        "house_edge_minimum": 10.0,
    },
    "A0090": {
        "family_name": "A0090_live_shell",
        "arm_threshold": 60.0,
        "enter_threshold": 68.0,
        "reduce_threshold": 54.0,
        "exit_threshold": 60.0,
        "natal_activation_minimum": 40.0,
        "friction_minimum": 60.0,
        "benefic_support_minimum": 62.0,
        "malefic_pressure_minimum": 60.0,
        "house_edge_minimum": 8.0,
    },
}

THRESHOLD_PROFILE_KEYS = {
    "A0001": "A0001",
    "A0002": "A0002",
    "A0003": "A0003",
    "A0004": "A0004",
    "A0090": "A0090",
}


@dataclass
class ThresholdProfile:
    family_name: str
    arm_threshold: float
    enter_threshold: float
    reduce_threshold: float
    exit_threshold: float
    natal_activation_minimum: float
    friction_minimum: float
    benefic_support_minimum: float
    malefic_pressure_minimum: float
    house_edge_minimum: float


@dataclass
class PureSignal:
    doctrine_id: str
    schema_version: str
    entry_score: float
    exit_score: float
    long_bias_score: float
    short_bias_score: float
    path_score: float
    friction_score: float
    volatility_score: float
    natal_activation_score: float
    macro_timing_score: float
    meso_timing_score: float
    micro_timing_score: float
    minute_window_score: float
    minute_exhaustion_score: float
    benefic_support_score: float
    malefic_pressure_score: float
    angular_power_score: float
    house_lift_score: float
    house_drag_score: float
    direction_name: str
    regime_name: str
    sect_name: str
    trigger_state: str
    entry_signal: str
    exit_signal: str
    macro_context: str
    meso_context: str
    micro_context: str
    minute_context: str
    doctrine_context: str
    astro_trade_key: str
    astro_language: str


@dataclass
class ExecState:
    family_name: str
    phase: str = "wait"
    position_direction: str = "flat"
    action: str = "wait"
    hold_bars: int = 0
    last_reason: str = ""


def clamp(x: float) -> float:
    return max(0.0, min(100.0, x))


def avg(*values: float) -> float:
    if not values:
        return 0.0
    return clamp(sum(values) / len(values))


def bucket5(score: float) -> str:
    if score < 20.0:
        return "very_low"
    if score < 40.0:
        return "low"
    if score < 60.0:
        return "mid"
    if score < 80.0:
        return "high"
    return "very_high"


def as_float(row: dict, key: str, default: float = 0.0) -> float:
    try:
        return float(row.get(key, "") or default)
    except ValueError:
        return default


def as_int(row: dict, key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, "") or default))
    except ValueError:
        return default


def safe(text: str) -> str:
    return text.replace('"', "'").replace(",", ";").replace("\r", " ").replace("\n", " ")


def aspect_score(row: dict, pair: str, *, soft: bool) -> float:
    aspect = (row.get(f"{pair}_aspect", "") or "").strip()
    orb_limit = max(0.0001, as_float(row, "aspect_orb_limit", 6.0))
    orb = as_float(row, f"{pair}_orb", 999.0)
    applying = as_int(row, f"{pair}_applying", 0)
    if orb > orb_limit:
        return 0.0
    valid = aspect in SOFT_ASPECTS if soft else aspect in HARD_ASPECTS
    if not valid:
        return 0.0
    tight = 100.0 * (1.0 - orb / orb_limit)
    if applying == 1:
        tight *= 1.05
    return clamp(tight)


def decl_score(row: dict, pair: str) -> float:
    relation = (row.get(f"{pair}_decl_relation", "") or "").strip()
    orb_limit = max(0.0001, as_float(row, "parallel_orb_limit", 1.0))
    orb = as_float(row, f"{pair}_decl_orb", 999.0)
    applying = as_int(row, f"{pair}_decl_applying", 0)
    if relation not in {"parallel", "contra_parallel"} or orb > orb_limit:
        return 0.0
    tight = 100.0 * (1.0 - orb / orb_limit)
    if applying == 1:
        tight *= 1.05
    if relation == "contra_parallel":
        tight *= 0.95
    return clamp(tight)


def station_risk(body: str, speed_lon: float) -> float:
    eps = {
        "moon": 0.45,
        "mercury": 0.08,
        "venus": 0.04,
        "mars": 0.025,
        "jupiter": 0.01,
        "saturn": 0.006,
        "uranus": 0.003,
        "neptune": 0.002,
        "pluto": 0.0015,
    }.get(body, 0.01)
    v = abs(speed_lon)
    if v <= eps:
        return 100.0
    if v <= eps * 2.0:
        return 70.0
    if v <= eps * 4.0:
        return 35.0
    return 0.0


def ingress_intensity(degree_in_sign: float) -> float:
    near = min(degree_in_sign, 30.0 - degree_in_sign)
    if near <= 0.25:
        return 100.0
    if near <= 0.50:
        return 80.0
    if near <= 1.00:
        return 60.0
    if near <= 2.00:
        return 30.0
    return 0.0


def house_angularity(house: int) -> float:
    return HOUSE_ANGULARITY.get(house, 0.0)


def house_lift(house: int) -> float:
    if house == 10:
        return 100.0
    if house in {1, 11}:
        return 92.0
    if house in {5, 9}:
        return 78.0
    if house in {2, 7}:
        return 62.0
    if house in {3, 4}:
        return 46.0
    if house in {6, 8}:
        return 26.0
    if house == 12:
        return 18.0
    return 40.0


def house_drag(house: int) -> float:
    if house == 12:
        return 100.0
    if house in {8, 6}:
        return 84.0
    if house == 4:
        return 70.0
    if house == 3:
        return 52.0
    if house in {7, 2}:
        return 40.0
    if house in {9, 5}:
        return 28.0
    if house in {11, 1}:
        return 18.0
    if house == 10:
        return 12.0
    return 40.0


def dignity_score(body: str, sign: str) -> float:
    if body == "sun":
        if sign == "leo":
            return 95.0
        if sign == "aries":
            return 86.0
        if sign == "aquarius":
            return 18.0
        if sign == "libra":
            return 10.0
    if body == "moon":
        if sign == "cancer":
            return 95.0
        if sign == "taurus":
            return 86.0
        if sign == "capricorn":
            return 18.0
        if sign == "scorpio":
            return 10.0
    if body == "mercury":
        if sign in {"gemini", "virgo"}:
            return 92.0
        if sign == "pisces":
            return 10.0
        if sign in {"sagittarius", "pisces"}:
            return 18.0
    if body == "venus":
        if sign in {"taurus", "libra"}:
            return 92.0
        if sign == "pisces":
            return 96.0
        if sign in {"scorpio", "aries"}:
            return 18.0
        if sign == "virgo":
            return 10.0
    if body == "mars":
        if sign in {"aries", "scorpio"}:
            return 92.0
        if sign == "capricorn":
            return 96.0
        if sign in {"libra", "taurus"}:
            return 18.0
        if sign == "cancer":
            return 10.0
    if body == "jupiter":
        if sign in {"sagittarius", "pisces"}:
            return 92.0
        if sign == "cancer":
            return 96.0
        if sign in {"gemini", "virgo"}:
            return 18.0
        if sign == "capricorn":
            return 10.0
    if body == "saturn":
        if sign in {"capricorn", "aquarius"}:
            return 92.0
        if sign == "libra":
            return 96.0
        if sign in {"cancer", "leo"}:
            return 18.0
        if sign == "aries":
            return 10.0
    return 50.0


def sect_favorability(body: str, diurnal: bool) -> float:
    if body == "sun":
        return 96.0 if diurnal else 34.0
    if body == "moon":
        return 38.0 if diurnal else 96.0
    if body == "jupiter":
        return 92.0 if diurnal else 60.0
    if body == "venus":
        return 62.0 if diurnal else 92.0
    if body == "saturn":
        return 78.0 if diurnal else 28.0
    if body == "mars":
        return 28.0 if diurnal else 76.0
    if body == "mercury":
        return 64.0
    return 50.0


def speed_intensity(speed_lon: float, normal_speed: float) -> float:
    if normal_speed <= 0.0:
        return 0.0
    return clamp(50.0 * abs(speed_lon) / normal_speed)


def phase_boundary_near(angle: float, orb_deg: float = 5.0) -> bool:
    boundaries = (0.0, 90.0, 180.0, 270.0, 360.0)
    return any(abs(angle - b) <= orb_deg for b in boundaries)


def sign_element(sign: str) -> str:
    return SIGN_ELEMENT.get(sign, "water")


def sign_modality(sign: str) -> str:
    return SIGN_MODALITY.get(sign, "mutable")


def transit_natal_resonance(row: dict) -> float:
    if as_int(row, "natal_enabled", 0) != 1:
        return 0.0
    score = 0.0
    for name in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
        score += 0.08 * house_angularity(as_int(row, f"{name}_in_natal_house", -1))
    orb_limit = max(0.0001, as_float(row, "aspect_orb_limit", 6.0))
    for t_name in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
        for n_name in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
            key = f"t_{t_name}__n_{n_name}"
            aspect = (row.get(f"{key}_aspect", "") or "").strip()
            orb = as_float(row, f"{key}_orb", 999.0)
            if aspect == "none" or orb > orb_limit:
                continue
            tight = 100.0 * (1.0 - orb / orb_limit)
            if as_int(row, f"{key}_applying", 0) == 1:
                tight *= 1.05
            score += 0.03 * clamp(tight)
    return clamp(score)


def compute_signal(row: dict) -> PureSignal:
    signs = [row.get(f"{name}_sign", "") for name in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn")]
    fire_air = sum(1 for s in signs if sign_element(s) in {"fire", "air"})
    earth_water = sum(1 for s in signs if sign_element(s) in {"earth", "water"})
    cardinal = sum(1 for s in signs if sign_modality(s) == "cardinal")
    fixed = sum(1 for s in signs if sign_modality(s) == "fixed")

    expansion_bias = clamp(100.0 * fire_air / 7.0)
    compression_bias = clamp(100.0 * earth_water / 7.0)
    cardinal_bias = clamp(100.0 * cardinal / 7.0)
    fixed_bias = clamp(100.0 * fixed / 7.0)

    js_soft = aspect_score(row, "jupiter_saturn", soft=True)
    js_hard = aspect_score(row, "jupiter_saturn", soft=False)
    sun_sat_hard = aspect_score(row, "sun_saturn", soft=False)
    sun_jup_soft = aspect_score(row, "sun_jupiter", soft=True)
    moon_jup_soft = aspect_score(row, "moon_jupiter", soft=True)
    moon_sat_hard = aspect_score(row, "moon_saturn", soft=False)
    moon_mars_hard = aspect_score(row, "moon_mars", soft=False)
    sun_moon_soft = aspect_score(row, "sun_moon", soft=True)
    sun_moon_hard = aspect_score(row, "sun_moon", soft=False)
    sun_mars_soft = aspect_score(row, "sun_mars", soft=True)
    sun_mars_hard = aspect_score(row, "sun_mars", soft=False)
    moon_venus_soft = aspect_score(row, "moon_venus", soft=True)
    moon_mercury_hard = aspect_score(row, "moon_mercury", soft=False)
    sun_mercury_hard = aspect_score(row, "sun_mercury", soft=False)
    venus_mars_soft = aspect_score(row, "venus_mars", soft=True)
    venus_mars_hard = aspect_score(row, "venus_mars", soft=False)
    mars_sat_hard = aspect_score(row, "mars_saturn", soft=False)
    mars_sat_soft = aspect_score(row, "mars_saturn", soft=True)

    moon_deg = as_float(row, "moon_degree")
    jupiter_deg = as_float(row, "jupiter_degree")
    saturn_deg = as_float(row, "saturn_degree")
    uranus_deg = as_float(row, "uranus_degree")
    mercury_deg = as_float(row, "mercury_degree")
    mars_deg = as_float(row, "mars_degree")

    outer_station_risk = avg(
        station_risk("uranus", as_float(row, "uranus_speed_lon")),
        station_risk("neptune", as_float(row, "neptune_speed_lon")),
        station_risk("pluto", as_float(row, "pluto_speed_lon")),
    )
    macro_transition = avg(
        outer_station_risk,
        ingress_intensity(jupiter_deg),
        ingress_intensity(saturn_deg),
        ingress_intensity(uranus_deg),
    )
    macro_flow = clamp(0.45 * js_soft + 0.25 * sun_jup_soft + 0.20 * expansion_bias + 0.10 * (100.0 - macro_transition))
    macro_pressure = clamp(0.55 * js_hard + 0.30 * sun_sat_hard + 0.15 * macro_transition)
    macro_drag = clamp(0.45 * station_risk("saturn", as_float(row, "saturn_speed_lon")) + 0.25 * compression_bias + 0.20 * fixed_bias + 0.10 * macro_transition)
    macro_expansion = clamp(0.45 * expansion_bias + 0.30 * cardinal_bias + 0.25 * macro_flow)
    macro_compression = clamp(0.45 * compression_bias + 0.30 * macro_drag + 0.25 * fixed_bias)
    structural_bias = clamp(macro_expansion - 0.35 * macro_compression + 30.0)

    mars_sign = row.get("mars_sign", "")
    sun_house = as_int(row, "sun_house", -1)
    moon_house = as_int(row, "moon_house", -1)
    mercury_house = as_int(row, "mercury_house", -1)
    venus_house = as_int(row, "venus_house", -1)
    mars_house = as_int(row, "mars_house", -1)
    jupiter_house = as_int(row, "jupiter_house", -1)
    saturn_house = as_int(row, "saturn_house", -1)
    diurnal_sect = 7 <= sun_house <= 12
    sect_name = "day" if diurnal_sect else "night"

    benefic_support_score = clamp(avg(
        0.42 * dignity_score("venus", row.get("venus_sign", "")) + 0.28 * house_lift(venus_house) + 0.20 * sect_favorability("venus", diurnal_sect) + 0.10 * (30.0 if as_int(row, "venus_retro", 0) == 1 else 72.0),
        0.42 * dignity_score("jupiter", row.get("jupiter_sign", "")) + 0.28 * house_lift(jupiter_house) + 0.20 * sect_favorability("jupiter", diurnal_sect) + 0.10 * (38.0 if as_int(row, "jupiter_retro", 0) == 1 else 70.0),
    ))
    malefic_pressure_score = clamp(avg(
        0.44 * dignity_score("mars", row.get("mars_sign", "")) + 0.22 * house_drag(mars_house) + 0.22 * (100.0 - sect_favorability("mars", diurnal_sect)) + 0.12 * (56.0 if as_int(row, "mars_retro", 0) == 1 else 72.0),
        0.44 * dignity_score("saturn", row.get("saturn_sign", "")) + 0.22 * house_drag(saturn_house) + 0.22 * (100.0 - sect_favorability("saturn", diurnal_sect)) + 0.12 * (46.0 if as_int(row, "saturn_retro", 0) == 1 else 68.0),
    ))
    angular_power_score = clamp(
        0.22 * house_angularity(sun_house) +
        0.18 * house_angularity(moon_house) +
        0.15 * house_angularity(venus_house) +
        0.15 * house_angularity(mars_house) +
        0.15 * house_angularity(jupiter_house) +
        0.15 * house_angularity(saturn_house)
    )
    house_lift_score = clamp(
        0.25 * house_lift(sun_house) +
        0.15 * house_lift(moon_house) +
        0.10 * house_lift(mercury_house) +
        0.10 * house_lift(venus_house) +
        0.15 * house_lift(mars_house) +
        0.15 * house_lift(jupiter_house) +
        0.10 * house_lift(saturn_house)
    )
    house_drag_score = clamp(
        0.20 * house_drag(sun_house) +
        0.18 * house_drag(moon_house) +
        0.10 * house_drag(venus_house) +
        0.16 * house_drag(mars_house) +
        0.12 * house_drag(jupiter_house) +
        0.24 * house_drag(saturn_house)
    )
    doctrine_context = (
        f"sect={sect_name}"
        f"|benefic={bucket5(benefic_support_score)}"
        f"|malefic={bucket5(malefic_pressure_score)}"
        f"|angular={bucket5(angular_power_score)}"
        f"|lift={bucket5(house_lift_score)}"
        f"|drag={bucket5(house_drag_score)}"
    )

    mars_speed = speed_intensity(as_float(row, "mars_speed_lon"), 0.55)
    moon_speed = speed_intensity(as_float(row, "moon_speed_lon"), 13.2)
    mars_direct_bonus = 0.0 if as_int(row, "mars_retro", 0) == 1 else 20.0
    mars_element_bonus = 16.0 if sign_element(mars_sign) in {"fire", "air"} else 8.0 if sign_element(mars_sign) == "earth" else 0.0
    mars_impulse = clamp(0.60 * mars_speed + mars_direct_bonus + mars_element_bonus + 0.20 * cardinal_bias + 0.15 * sun_mars_soft + 0.10 * sun_mars_hard)
    mars_saturn_friction = clamp(0.70 * mars_sat_hard + 0.20 * station_risk("saturn", as_float(row, "saturn_speed_lon")) + 0.10 * station_risk("saturn", as_float(row, "saturn_speed_lon")) - 0.20 * mars_sat_soft)
    jupiter_support = clamp(0.45 * sun_jup_soft + 0.35 * js_soft + 0.20 * expansion_bias)
    mars_jupiter_expansion = clamp(0.55 * mars_impulse + 0.45 * jupiter_support)
    saturn_resistance = clamp(0.55 * station_risk("saturn", as_float(row, "saturn_speed_lon")) + 0.30 * mars_saturn_friction + 0.15 * station_risk("saturn", as_float(row, "saturn_speed_lon")))

    mercury_station = station_risk("mercury", as_float(row, "mercury_speed_lon"))
    mercury_retro = 70.0 if as_int(row, "mercury_retro", 0) == 1 else 0.0
    mercury_noise = clamp(0.35 * mercury_station + 0.30 * mercury_retro + 0.20 * moon_mercury_hard + 0.15 * sun_mercury_hard)
    venus_mars_cohesion = clamp(0.65 * venus_mars_soft + 0.20 * (100.0 - venus_mars_hard) + 0.15 * (100.0 - mercury_noise))
    mars_clean_impulse = clamp(0.55 * mars_impulse + 0.20 * venus_mars_cohesion + 0.15 * jupiter_support - 0.35 * mars_saturn_friction - 0.20 * mercury_noise + 25.0)

    moon_pressure = clamp(0.45 * moon_mars_hard + 0.35 * moon_sat_hard + 0.20 * sun_moon_hard)
    moon_flow = clamp(0.40 * sun_moon_soft + 0.35 * moon_jup_soft + 0.25 * moon_venus_soft)
    moon_drag = clamp(0.65 * moon_sat_hard + 0.25 * station_risk("saturn", as_float(row, "saturn_speed_lon")) + 0.10 * station_risk("saturn", as_float(row, "saturn_speed_lon")))
    moon_boundary = avg(
        ingress_intensity(moon_deg),
        80.0 if phase_boundary_near(as_float(row, "moon_phase_angle"), 5.0) else 0.0,
        station_risk("moon", as_float(row, "moon_speed_lon")),
    )
    moon_oob_intensity = clamp(20.0 + 20.0 * max(0.0, abs(as_float(row, "moon_decl")) - 23.44)) if as_int(row, "moon_oob", 0) == 1 else 0.0
    micro_noise = clamp(0.30 * moon_pressure + 0.25 * moon_boundary + 0.20 * mercury_noise + 0.15 * moon_oob_intensity + 0.10 * macro_pressure)
    micro_cleanliness = clamp(0.35 * moon_flow + 0.25 * moon_speed + 0.20 * (100.0 - micro_noise) + 0.20 * (100.0 - moon_drag))

    pullback_risk = clamp(0.35 * moon_drag + 0.25 * micro_noise + 0.20 * mars_saturn_friction + 0.20 * macro_drag)
    chop_risk = clamp(0.30 * macro_transition + 0.25 * mercury_noise + 0.20 * moon_boundary + 0.15 * micro_noise + 0.10 * macro_pressure)
    clean_impulse = clamp(0.40 * mars_clean_impulse + 0.25 * micro_cleanliness + 0.20 * (100.0 - pullback_risk) + 0.15 * (100.0 - macro_drag))
    smooth_continuation = clamp(0.35 * macro_flow + 0.30 * moon_flow + 0.20 * (100.0 - saturn_resistance) + 0.15 * venus_mars_cohesion)
    breakout_followthrough = clamp(0.35 * mars_jupiter_expansion + 0.25 * moon_speed + 0.20 * clean_impulse + 0.20 * (100.0 - micro_noise))
    clean_path = clamp(0.30 * clean_impulse + 0.25 * smooth_continuation + 0.20 * (100.0 - pullback_risk) + 0.15 * (100.0 - chop_risk) + 0.10 * moon_flow)
    m1_clean_window = clamp(0.35 * clean_path + 0.25 * micro_cleanliness + 0.20 * breakout_followthrough + 0.20 * (100.0 - pullback_risk))
    m1_dirty_window = clamp(0.35 * pullback_risk + 0.35 * chop_risk + 0.20 * micro_noise + 0.10 * macro_transition)

    mars_ang = house_angularity(as_int(row, "mars_house", -1))
    moon_ang = house_angularity(as_int(row, "moon_house", -1))
    sun_ang = house_angularity(as_int(row, "sun_house", -1))
    jupiter_ang = house_angularity(as_int(row, "jupiter_house", -1))
    saturn_ang = house_angularity(as_int(row, "saturn_house", -1))

    macro_long = 0.42 * macro_flow + 0.24 * macro_expansion + 0.20 * jupiter_support + 0.14 * (100.0 - macro_pressure)
    macro_short = 0.38 * macro_drag + 0.28 * macro_pressure + 0.18 * macro_compression + 0.16 * saturn_resistance
    macro_bias_score = clamp(abs(macro_long - macro_short))
    macro_alignment_score = clamp(0.34 * (100.0 - macro_transition) + 0.24 * structural_bias + 0.22 * max(mars_ang, sun_ang) + 0.20 * max(jupiter_ang, saturn_ang))
    macro_direction = "long" if macro_long >= macro_short + 6.0 else "short" if macro_short >= macro_long + 6.0 else "flat"

    meso_angularity_score = clamp(0.30 * mars_ang + 0.25 * moon_ang + 0.20 * sun_ang + 0.15 * jupiter_ang + 0.10 * saturn_ang)
    meso_resonance_score = clamp(
        0.26 * transit_natal_resonance(row) +
        0.18 * decl_score(row, "sun_moon") +
        0.18 * decl_score(row, "venus_mars") +
        0.20 * decl_score(row, "mars_saturn") +
        0.18 * decl_score(row, "jupiter_saturn")
    )
    meso_gate_score = clamp(0.42 * meso_angularity_score + 0.28 * meso_resonance_score + 0.15 * clean_path + 0.15 * (100.0 - chop_risk))

    micro_trigger_score = clamp(0.26 * moon_speed + 0.24 * moon_flow + 0.16 * (100.0 - moon_boundary) + 0.18 * (100.0 - micro_noise) + 0.16 * breakout_followthrough)
    micro_release_score = clamp(0.28 * clean_impulse + 0.20 * mars_clean_impulse + 0.18 * venus_mars_cohesion + 0.18 * (100.0 - pullback_risk) + 0.16 * (100.0 - moon_drag))
    minute_window_score = clamp(0.28 * micro_trigger_score + 0.22 * micro_release_score + 0.20 * m1_clean_window + 0.12 * decl_score(row, "moon_mars") + 0.10 * (100.0 - mercury_station) + 0.08 * (100.0 - m1_dirty_window))
    minute_exhaustion_score = clamp(0.26 * m1_dirty_window + 0.22 * pullback_risk + 0.20 * moon_boundary + 0.16 * macro_transition + 0.16 * mercury_station)

    trigger_state = "standby"
    if macro_direction != "flat" and macro_alignment_score >= 58.0 and meso_gate_score >= 54.0:
        trigger_state = "armed"
    if macro_direction != "flat" and macro_alignment_score >= 62.0 and meso_gate_score >= 60.0 and minute_window_score >= 64.0 and minute_exhaustion_score <= 44.0:
        trigger_state = "trigger_ready"
    if minute_exhaustion_score >= 62.0:
        trigger_state = "timing_exit"

    long_bias_score = clamp(
        0.32 * mars_impulse +
        0.22 * jupiter_support +
        0.18 * moon_flow +
        0.18 * (100.0 if sign_element(mars_sign) == "fire" else 75.0 if sign_element(mars_sign) == "air" else 40.0 if sign_element(mars_sign) == "earth" else 50.0) +
        0.10 * (95.0 if sign_modality(mars_sign) == "cardinal" else 65.0 if sign_modality(mars_sign) == "fixed" else 55.0) +
        0.12 * benefic_support_score +
        0.10 * house_lift_score +
        0.06 * angular_power_score
    )
    short_bias_score = clamp(
        0.35 * saturn_resistance +
        0.25 * mars_saturn_friction +
        0.20 * moon_pressure +
        0.10 * (100.0 - jupiter_support) +
        0.10 * (80.0 if sign_element(row.get("moon_sign", "")) == "water" else 45.0) +
        0.14 * malefic_pressure_score +
        0.10 * house_drag_score +
        0.04 * (100.0 - benefic_support_score)
    )
    if as_int(row, "mars_oob", 0) == 1:
        long_bias_score = clamp(long_bias_score + 4.0)
    if as_int(row, "saturn_oob", 0) == 1:
        short_bias_score = clamp(short_bias_score + 4.0)

    natal_activation_score = 0.0
    if as_int(row, "natal_enabled", 0) == 1:
        def tn_score(key: str) -> float:
            aspect = (row.get(f"{key}_aspect", "") or "").strip()
            orb = as_float(row, f"{key}_orb", 999.0)
            orb_limit = max(0.0001, as_float(row, "aspect_orb_limit", 6.0))
            if aspect == "none" or orb > 6.0:
                return 0.0
            tight = 100.0 * (1.0 - orb / 6.0)
            if as_int(row, f"{key}_applying", 0) == 1:
                tight *= 1.10
            return clamp(tight)
        def tn_decl(key: str) -> float:
            relation = (row.get(f"{key}_decl_relation", "") or "").strip()
            orb = as_float(row, f"{key}_decl_orb", 999.0)
            orb_limit = max(0.0001, as_float(row, "parallel_orb_limit", 1.0))
            if relation not in {"parallel", "contra_parallel"} or orb > orb_limit:
                return 0.0
            tight = 100.0 * (1.0 - orb / orb_limit)
            if as_int(row, f"{key}_decl_applying", 0) == 1:
                tight *= 1.05
            if relation == "contra_parallel":
                tight *= 0.95
            return clamp(tight)
        natal_activation_score = clamp(
            0.35 * tn_score("t_sun__n_sun") +
            0.10 * tn_decl("t_sun__n_sun") +
            0.25 * tn_score("t_moon__n_moon") +
            0.10 * tn_decl("t_moon__n_moon") +
            0.20 * tn_score("t_mars__n_saturn") +
            0.10 * tn_decl("t_mars__n_saturn") +
            0.20 * tn_score("t_jupiter__n_mars")
        )

    direction_name = macro_direction
    if direction_name == "flat":
        if long_bias_score >= short_bias_score + 8.0:
            direction_name = "long"
        elif short_bias_score >= long_bias_score + 8.0:
            direction_name = "short"

    friction_score = clamp(chop_risk + 0.18 * malefic_pressure_score + 0.08 * house_drag_score)
    volatility_score = clamp(avg(breakout_followthrough, macro_pressure, macro_transition))
    regime_name = "clean" if clean_path >= 70.0 and friction_score <= 40.0 and minute_window_score >= 60.0 else "volatile" if volatility_score >= 70.0 and micro_trigger_score >= 56.0 else "frictional" if friction_score >= 65.0 or minute_exhaustion_score >= 62.0 else "mixed"

    entry_score = clamp(
        0.24 * max(long_bias_score, short_bias_score) +
        0.08 * benefic_support_score +
        0.18 * clean_path +
        0.12 * volatility_score +
        0.14 * natal_activation_score +
        0.12 * macro_alignment_score +
        0.10 * meso_gate_score +
        0.10 * micro_trigger_score +
        0.08 * house_lift_score
    )
    exit_score = clamp(
        0.30 * friction_score +
        0.10 * malefic_pressure_score +
        0.22 * pullback_risk +
        0.16 * m1_dirty_window +
        0.16 * minute_exhaustion_score +
        0.08 * (100.0 - minute_window_score) +
        0.06 * house_drag_score
    )

    entry_signal = "wait"
    if direction_name == "long" and entry_score >= 66.0 and trigger_state == "trigger_ready":
        entry_signal = "enter_long"
    elif direction_name == "short" and entry_score >= 66.0 and trigger_state == "trigger_ready":
        entry_signal = "enter_short"
    elif trigger_state == "armed":
        entry_signal = "arm"
    exit_signal = "exit_or_reduce" if trigger_state == "timing_exit" or exit_score >= 58.0 else "hold"

    macro_context = f"macro:{macro_direction}|bias={bucket5(macro_bias_score)}|align={bucket5(macro_alignment_score)}|flow={bucket5(macro_flow)}|pressure={bucket5(macro_pressure)}"
    meso_context = f"meso:gate_{bucket5(meso_gate_score)}|angular={bucket5(meso_angularity_score)}|resonance={bucket5(meso_resonance_score)}"
    micro_context = f"micro:trigger_{bucket5(micro_trigger_score)}|release={bucket5(micro_release_score)}|tempo={bucket5(moon_speed)}|noise={bucket5(micro_noise)}"
    minute_context = f"minute:window_{bucket5(minute_window_score)}|exhaust={bucket5(minute_exhaustion_score)}|m1clean={bucket5(m1_clean_window)}|m1dirty={bucket5(m1_dirty_window)}"
    astro_language = (
        f"doctrine={row.get('doctrine_id','')}"
        f"|schema={row.get('schema_version','')}"
        f"|bias={row.get('astro_bias_text','')}"
        f"|path={row.get('astro_path_text','')}"
        f"|signal={row.get('astro_signal_text','')}"
        f"|sect={sect_name}"
        f"|dir={direction_name}"
        f"|regime={regime_name}"
        f"|ctx={doctrine_context}"
        f"|macro={macro_context}"
        f"|meso={meso_context}"
        f"|micro={micro_context}"
        f"|minute={minute_context}"
    )
    astro_trade_key = f"astro_trade{{dir={direction_name}|entry={entry_signal}|exit={exit_signal}|regime={regime_name}}}"

    return PureSignal(
        doctrine_id=row.get("doctrine_id", ""),
        schema_version=row.get("schema_version", ""),
        entry_score=entry_score,
        exit_score=exit_score,
        long_bias_score=long_bias_score,
        short_bias_score=short_bias_score,
        path_score=clean_path,
        friction_score=friction_score,
        volatility_score=volatility_score,
        natal_activation_score=natal_activation_score,
        macro_timing_score=macro_alignment_score,
        meso_timing_score=meso_gate_score,
        micro_timing_score=micro_trigger_score,
        minute_window_score=minute_window_score,
        minute_exhaustion_score=minute_exhaustion_score,
        benefic_support_score=benefic_support_score,
        malefic_pressure_score=malefic_pressure_score,
        angular_power_score=angular_power_score,
        house_lift_score=house_lift_score,
        house_drag_score=house_drag_score,
        direction_name=direction_name,
        regime_name=regime_name,
        sect_name=sect_name,
        trigger_state=trigger_state,
        entry_signal=entry_signal,
        exit_signal=exit_signal,
        macro_context=macro_context,
        meso_context=meso_context,
        micro_context=micro_context,
        minute_context=minute_context,
        doctrine_context=doctrine_context,
        astro_trade_key=astro_trade_key,
        astro_language=astro_language,
    )


def apply_family_gates(family: str, signal: PureSignal, row: dict, thresholds: ThresholdProfile) -> PureSignal:
    gated = PureSignal(**vars(signal))
    if family == "A0002":
        if as_int(row, "natal_enabled", 0) != 1 or gated.natal_activation_score < thresholds.natal_activation_minimum:
            gated.entry_signal = "wait"
    elif family == "A0003":
        if gated.friction_score < thresholds.friction_minimum:
            gated.entry_signal = "wait"
    elif family == "A0004":
        support_edge = gated.benefic_support_score - gated.malefic_pressure_score
        house_edge = gated.house_lift_score - gated.house_drag_score
        benefic_ok = (
            gated.benefic_support_score >= thresholds.benefic_support_minimum
            and support_edge >= thresholds.house_edge_minimum
            and house_edge >= thresholds.house_edge_minimum
        )
        malefic_ok = (
            gated.malefic_pressure_score >= thresholds.malefic_pressure_minimum
            and (-support_edge) >= thresholds.house_edge_minimum
            and (-house_edge) >= thresholds.house_edge_minimum
        )
        if benefic_ok:
            if gated.direction_name != "long":
                gated.entry_signal = "wait"
        elif malefic_ok:
            if gated.direction_name != "short":
                gated.entry_signal = "wait"
        else:
            gated.entry_signal = "wait"
    return gated


def step_state(state: ExecState, signal: PureSignal, thresholds: ThresholdProfile) -> ExecState:
    state.action = "wait"
    state.last_reason = signal.astro_language
    has_long = signal.entry_signal == "enter_long"
    has_short = signal.entry_signal == "enter_short"
    wants_exit = signal.exit_signal == "exit_or_reduce"
    opposite_long = state.position_direction == "short" and has_long
    opposite_short = state.position_direction == "long" and has_short

    if state.phase == "wait":
        if signal.entry_score >= thresholds.enter_threshold and (has_long or has_short):
            state.phase = "enter"
            state.position_direction = "long" if has_long else "short"
            state.action = "enter"
            state.hold_bars = 0
        elif signal.entry_score >= thresholds.arm_threshold and signal.direction_name != "flat":
            state.phase = "armed"
            state.position_direction = signal.direction_name
            state.action = "armed"
        return state

    if state.phase == "armed":
        if signal.entry_score >= thresholds.enter_threshold and (has_long or has_short):
            state.phase = "enter"
            state.position_direction = "long" if has_long else "short"
            state.action = "enter"
            state.hold_bars = 0
        elif signal.entry_score < thresholds.arm_threshold or signal.direction_name == "flat":
            state.phase = "wait"
            state.position_direction = "flat"
            state.action = "wait"
        return state

    if state.phase == "enter":
        state.phase = "hold"
        state.action = "hold"
        state.hold_bars = 1
        return state

    if state.phase == "hold":
        state.hold_bars += 1
        if wants_exit and signal.exit_score >= thresholds.exit_threshold:
            state.phase = "exit"
            state.action = "exit"
            return state
        if (opposite_long or opposite_short) and signal.entry_score >= thresholds.enter_threshold:
            state.phase = "exit"
            state.action = "exit"
            state.last_reason = signal.astro_language + "|collision=opposite_entry"
            return state
        if wants_exit and signal.exit_score >= thresholds.reduce_threshold:
            state.phase = "reduce"
            state.action = "reduce"
            return state
        state.action = "hold"
        return state

    if state.phase == "reduce":
        state.hold_bars += 1
        if wants_exit and signal.exit_score >= thresholds.exit_threshold:
            state.phase = "exit"
            state.action = "exit"
            return state
        if signal.entry_score >= thresholds.enter_threshold and signal.direction_name == state.position_direction:
            state.phase = "hold"
            state.action = "hold"
            return state
        state.action = "reduce"
        return state

    if state.phase == "exit":
        state.phase = "wait"
        state.position_direction = "flat"
        state.action = "wait"
        state.hold_bars = 0
        return state

    return state


def iter_rows(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8", newline="") as f:
        yield from csv.DictReader(f)


def load_config(path: str) -> Dict[str, object]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def resolve_thresholds(family: str, config: Optional[Dict[str, object]]) -> ThresholdProfile:
    base = dict(FAMILY_DEFAULTS[family])
    if config:
        profiles = config.get("threshold_profiles", {})
        if isinstance(profiles, dict):
            extra = profiles.get(THRESHOLD_PROFILE_KEYS[family], {})
            if isinstance(extra, dict):
                for key in (
                    "arm_threshold",
                    "enter_threshold",
                    "reduce_threshold",
                    "exit_threshold",
                    "natal_activation_minimum",
                    "friction_minimum",
                    "benefic_support_minimum",
                    "malefic_pressure_minimum",
                    "house_edge_minimum",
                ):
                    if key in extra:
                        base[key] = float(extra[key])
    return ThresholdProfile(**base)


def journal_header() -> List[str]:
    return [
        "broker_time", "utc_time", "family_name", "doctrine_id", "schema_version", "phase", "action",
        "position_direction", "entry_signal", "exit_signal", "direction_name", "regime_name", "entry_score",
        "exit_score", "long_bias_score", "short_bias_score", "path_score", "friction_score", "volatility_score",
        "natal_activation_score", "macro_timing_score", "meso_timing_score", "micro_timing_score",
        "minute_window_score", "minute_exhaustion_score", "trigger_state", "macro_context", "meso_context",
        "micro_context", "minute_context", "feature_key", "astro_trade_key", "astro_language", "reason", "hold_bars",
    ]


def row_to_journal(row: dict, signal: PureSignal, state: ExecState) -> Dict[str, object]:
    return {
        "broker_time": row.get("broker_time", ""),
        "utc_time": row.get("utc_time", ""),
        "family_name": state.family_name,
        "doctrine_id": signal.doctrine_id,
        "schema_version": signal.schema_version,
        "phase": state.phase,
        "action": state.action,
        "position_direction": state.position_direction,
        "entry_signal": signal.entry_signal,
        "exit_signal": signal.exit_signal,
        "direction_name": signal.direction_name,
        "regime_name": signal.regime_name,
        "entry_score": f"{signal.entry_score:.4f}",
        "exit_score": f"{signal.exit_score:.4f}",
        "long_bias_score": f"{signal.long_bias_score:.4f}",
        "short_bias_score": f"{signal.short_bias_score:.4f}",
        "path_score": f"{signal.path_score:.4f}",
        "friction_score": f"{signal.friction_score:.4f}",
        "volatility_score": f"{signal.volatility_score:.4f}",
        "natal_activation_score": f"{signal.natal_activation_score:.4f}",
        "macro_timing_score": f"{signal.macro_timing_score:.4f}",
        "meso_timing_score": f"{signal.meso_timing_score:.4f}",
        "micro_timing_score": f"{signal.micro_timing_score:.4f}",
        "minute_window_score": f"{signal.minute_window_score:.4f}",
        "minute_exhaustion_score": f"{signal.minute_exhaustion_score:.4f}",
        "trigger_state": signal.trigger_state,
        "macro_context": safe(signal.macro_context),
        "meso_context": safe(signal.meso_context),
        "micro_context": safe(signal.micro_context),
        "minute_context": safe(signal.minute_context),
        "feature_key": safe(row.get("feature_key", "")),
        "astro_trade_key": safe(signal.astro_trade_key),
        "astro_language": safe(signal.astro_language),
        "reason": safe(state.last_reason),
        "hold_bars": state.hold_bars,
    }


def run_family(csv_path: Path, family: str, out_journal: Path, config: Optional[Dict[str, object]]) -> Dict[str, object]:
    thresholds = resolve_thresholds(family, config)
    state = ExecState(family_name=thresholds.family_name)
    count = 0
    entered = 0
    exited = 0

    out_journal.parent.mkdir(parents=True, exist_ok=True)
    with out_journal.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=journal_header())
        writer.writeheader()
        for row in iter_rows(csv_path):
            signal = compute_signal(row)
            signal = apply_family_gates(family, signal, row, thresholds)
            prior_action = state.action
            state = step_state(state, signal, thresholds)
            if state.action == "enter":
                entered += 1
            if state.action == "exit":
                exited += 1
            writer.writerow(row_to_journal(row, signal, state))
            count += 1

    return {
        "family": family,
        "family_name": thresholds.family_name,
        "rows": count,
        "entries": entered,
        "exits": exited,
        "journal": str(out_journal),
        "thresholds": vars(thresholds),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Astro feature CSV produced by astro_feature_builder.py")
    ap.add_argument("--family", required=True, choices=sorted(FAMILY_DEFAULTS.keys()))
    ap.add_argument("--out-journal", required=True, help="Output paper journal CSV path")
    ap.add_argument("--config", default="", help="Optional doctrine/threshold JSON config")
    args = ap.parse_args()

    config = load_config(args.config) if args.config else None
    report = run_family(Path(args.csv), args.family, Path(args.out_journal), config)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
