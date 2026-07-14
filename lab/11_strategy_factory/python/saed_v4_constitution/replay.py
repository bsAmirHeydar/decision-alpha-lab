"""Deterministic replay of constitutional requests."""
from __future__ import annotations

from typing import Iterable

from .models import AuthorityRequest, EvidenceUseRequest, ConstitutionalDecision
from .policy import ConstitutionKernel


def replay_authority(kernel: ConstitutionKernel, requests: Iterable[AuthorityRequest]) -> tuple[ConstitutionalDecision, ...]:
    ordered = sorted(requests, key=lambda x: (x.known_time, x.request_id))
    return tuple(kernel.evaluate_authority(x) for x in ordered)


def replay_evidence(kernel: ConstitutionKernel, requests: Iterable[EvidenceUseRequest]) -> tuple[ConstitutionalDecision, ...]:
    ordered = sorted(requests, key=lambda x: (x.known_time, x.request_id))
    return tuple(kernel.evaluate_evidence(x) for x in ordered)
