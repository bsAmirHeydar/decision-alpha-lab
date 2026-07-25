from __future__ import annotations
from dataclasses import dataclass
from enum import StrEnum
from typing import Optional
class LevelSide(StrEnum): HIGH="HIGH"; LOW="LOW"
class DataStatus(StrEnum): VALID="VALID"; STALE_OR_IMPUTED="STALE_OR_IMPUTED"; MISSING="MISSING"
class EvaluationStatus(StrEnum): CONFIRMED="CONFIRMED"; NO_EVENT="NO_EVENT"; UNCONFIRMED="UNCONFIRMED"; INVALID_PRICE_BASIS_MISMATCH="INVALID_PRICE_BASIS_MISMATCH"; INSUFFICIENT_HISTORY="INSUFFICIENT_HISTORY"
class ReferenceState(StrEnum): UNTOUCHED_BOTH="UNTOUCHED_BOTH"; ONE_SIDE_TOUCHED="ONE_SIDE_TOUCHED"; DIVERGENCE_CONFIRMED="DIVERGENCE_CONFIRMED"; BOTH_SIDES_TOUCHED="BOTH_SIDES_TOUCHED"; REFERENCE_EXHAUSTED="REFERENCE_EXHAUSTED"; UNCONFIRMED="UNCONFIRMED"
@dataclass(frozen=True)
class SymbolObservation:
 symbol:str; touched:bool; first_touch_time:Optional[str]; data_status:DataStatus
