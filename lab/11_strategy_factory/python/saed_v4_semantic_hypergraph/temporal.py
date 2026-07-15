from __future__ import annotations

from .canonical import parse_time
from .errors import TemporalBoundaryError


def validate_boundary(event_time: str, known_time: str, event_as_of: str, known_as_of: str) -> None:
    event = parse_time(event_time)
    known = parse_time(known_time)
    event_cutoff = parse_time(event_as_of)
    known_cutoff = parse_time(known_as_of)
    if event > event_cutoff:
        raise TemporalBoundaryError(f"event_time {event_time} exceeds event_as_of {event_as_of}")
    if known > known_cutoff:
        raise TemporalBoundaryError(f"known_time {known_time} exceeds known_as_of {known_as_of}")
    if known < event:
        raise TemporalBoundaryError("known_time cannot precede event_time")


def validate_interval(start: str, end: str, known_time: str, event_as_of: str, known_as_of: str) -> None:
    if parse_time(start) > parse_time(end):
        raise TemporalBoundaryError("edge event interval is inverted")
    validate_boundary(end, known_time, event_as_of, known_as_of)
