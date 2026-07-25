from __future__ import annotations
from .models import DatasetSnapshot
from .revisions import RevisionStore
from .snapshots import build_snapshot
from .errors import ReplayError
class SnapshotReplayer:
    def __init__(self,revisions:RevisionStore): self.revisions=revisions
    def replay(self,expected:DatasetSnapshot)->DatasetSnapshot:
        records=self.revisions.records_as_of(expected.known_as_of,expected.event_as_of)
        rebuilt=build_snapshot(records,expected.known_as_of,expected.event_as_of,expected.data_role,expected.lineage_root,expected.metadata)
        if rebuilt.snapshot_hash!=expected.snapshot_hash: raise ReplayError(f'snapshot mismatch: {rebuilt.snapshot_hash} != {expected.snapshot_hash}')
        return rebuilt
