from __future__ import annotations
from .canonical import content_hash,stable_id

def telemetry(cube)->dict:
    payload={'cube_hash':cube.cube_hash,'rows':cube.row_count,'ordinary_rows':cube.ordinary_row_count,'skip_rows':cube.skip_row_count,'abstain_rows':cube.abstain_row_count,'filled_rows':sum(r.filled for r in cube.rows),'ambiguous_rows':sum(r.ambiguous for r in cube.rows),'path_events':sum(len(r.path_events) for r in cube.rows),'source_observations':len(set(h for r in cube.rows for h in r.source_observation_hashes)),'complete_exposure':cube.complete_exposure,'production_authorization':False};payload['telemetry_id']=stable_id('cubetelemetry',payload);payload['telemetry_hash']=content_hash(payload);return payload
