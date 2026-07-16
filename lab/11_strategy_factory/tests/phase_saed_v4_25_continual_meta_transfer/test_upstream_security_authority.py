from __future__ import annotations

import copy

import pytest

from saed_v4_continual_meta_transfer.authority import boundary
from saed_v4_continual_meta_transfer.contracts import UpstreamIntakeContract
from saed_v4_continual_meta_transfer.errors import SecurityBoundaryError, UpstreamVerificationError
from saed_v4_continual_meta_transfer.security import scan
from saed_v4_continual_meta_transfer.upstream import verify


def test_upstream_verifies(config, upstream):
    receipt = verify(UpstreamIntakeContract.from_mapping(config["upstream_intake"]), upstream)
    assert receipt["scope_verified"]
    assert receipt["authority_denied"]


@pytest.mark.parametrize("path", ["handoff_hash", "certificate_hash", "research_policy_id"])
def test_upstream_identity_mutation_rejected(config, upstream, path):
    mutated = copy.deepcopy(config["upstream_intake"])
    mutated[path] = "0" * 64
    with pytest.raises(UpstreamVerificationError):
        verify(UpstreamIntakeContract.from_mapping(mutated), upstream)


def test_upstream_authority_mutation_rejected(config, upstream):
    mutated = copy.deepcopy(upstream)
    mutated["handoff"]["authority"]["runtime"] = True
    with pytest.raises(UpstreamVerificationError):
        verify(UpstreamIntakeContract.from_mapping(config["upstream_intake"]), mutated)


@pytest.mark.parametrize("payload", [
    {"api_key": "x"},
    {"nested": {"broker_token": "x"}},
    {"endpoint": "https://example.invalid"},
    ["wss://example.invalid"],
])
def test_security_scan_rejects_forbidden_surfaces(payload):
    with pytest.raises(SecurityBoundaryError):
        scan(payload)


def test_authority_boundary_is_all_false():
    result = boundary()
    assert not any(result["authority"].values())
    assert result["ucee_authority_preserved"]
    assert result["central_engine_mutation"] is False
