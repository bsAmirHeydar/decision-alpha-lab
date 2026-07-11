from dataclasses import replace
import pytest
from strategy_factory_governance.examples import reference_governance_bundle
from strategy_factory_governance import *

def test_reference_snapshot_and_release_are_consistent():
    scope,evidence,policy,evaluation,registry,entry,snapshot,release,report=reference_governance_bundle()
    snapshot.validate();release.validate();assert entry.entry_hash in snapshot.entry_hashes
    assert release.registry_snapshot_hash==snapshot.snapshot_hash
    assert release.model_artifact_hash==evidence.model_artifact_hash

def test_release_rejects_entry_not_in_snapshot():
    scope,evidence,policy,evaluation,registry,entry,snapshot,release,report=reference_governance_bundle()
    bad=replace(snapshot,entry_hashes=(),snapshot_hash="").with_hash()
    with pytest.raises(ValueError,match="absent"):
        build_release_manifest(entry,evidence,bad,release_version="2",channel=ReleaseChannel.INFERENCE_CANDIDATE,created_at_utc_msc=1)
