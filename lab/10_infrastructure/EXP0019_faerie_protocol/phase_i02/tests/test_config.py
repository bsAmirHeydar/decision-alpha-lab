from dataclasses import replace

import pytest

from fp_i02_kernel.config import ConfigurationBundle, ProjectionConfiguration, canonical_research_bundle
from fp_i02_kernel.enums import ContextProfile, ExecutionAuthority, QuotaConsumptionPolicy
from fp_i02_kernel.errors import FPI02Error


def test_canonical_research_bundle_has_no_live_authority():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    assert bundle.execution_authority() is ExecutionAuthority.NONE
    assert bundle.semantic.quota_consumption_policy is QuotaConsumptionPolicy.UNSET
    assert bundle.open_decision_ids == ("FP-DEC-012",)


def test_style_only_change_preserves_semantic_hash():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    changed = replace(bundle, projection=replace(bundle.projection, line_width=3, active_opacity=200))
    assert changed.semantic.config_hash == bundle.semantic.config_hash
    assert changed.projection.config_hash != bundle.projection.config_hash


def test_behavior_change_alters_semantic_hash():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    changed = replace(bundle.semantic, historical_n_depth=14)
    assert changed.config_hash != bundle.semantic.config_hash


def test_resolved_chart_timeframe_is_identity_bearing():
    h1 = canonical_research_bundle(resolved_confirmation_timeframe_seconds=3600, adapter_snapshot_hash="a" * 64)
    m15 = canonical_research_bundle(resolved_confirmation_timeframe_seconds=900, adapter_snapshot_hash="a" * 64)
    assert h1.semantic.config_hash != m15.semantic.config_hash
    assert h1.build_manifest(1).context_epoch_id != m15.build_manifest(1).context_epoch_id


def test_live_profile_is_blocked_while_q12_unset():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    with pytest.raises(FPI02Error) as exc:
        ConfigurationBundle(bundle.semantic, bundle.projection, bundle.operational, ContextProfile.CANONICAL_LIVE)
    assert exc.value.code == "FP_RC_OPEN_DECISION_BLOCKS_LIVE"


def test_paper_profile_is_permitted_without_live_authority():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    paper = replace(bundle, profile=ContextProfile.CANONICAL_PAPER)
    assert paper.execution_authority() is ExecutionAuthority.PAPER_ONLY


def test_invalid_projection_ranges_fail():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    with pytest.raises(FPI02Error):
        replace(bundle.projection, line_width=0)
    with pytest.raises(FPI02Error):
        replace(bundle.projection, active_opacity=300)


def test_calendar_day_policy_cannot_replace_missing_offsets():
    bundle = canonical_research_bundle(adapter_snapshot_hash="a" * 64)
    with pytest.raises(FPI02Error):
        replace(bundle.semantic, replace_missing_offsets=True)
