def test_one_retired_one_pending(output):assert output['retirement']['retired_count']==1 and output['retirement']['pending_count']==1
def test_retired_cell_is_128(output):assert output['retirement']['retired_records'][0]['cell_id']=='CELL_0128'
def test_pending_cell_is_127(output):assert output['retirement']['pending_candidates'][0]['cell_id']=='CELL_0127'
def test_retired_route_revoked(output):assert output['retirement']['retired_records'][0]['route_revoked'] is True
def test_retirement_tombstone(output):assert len(output['retirement']['retired_records'][0]['tombstone_hash'])==64
def test_reinstatement_prohibited(output):assert output['retirement']['reinstatement_without_requalification'] is False and output['retirement']['retired_records'][0]['reinstatement_allowed'] is False
def test_archive_immutable(output):assert output['archive']['immutable'] is True and output['archive']['packages'][0]['deletion_allowed'] is False
def test_post_retirement_verified(output):assert output['verification']['all_verified'] is True and output['verification']['verified_count']==1
def test_replacement_same_tenant(output):
 r=output['retirement']['retired_records'][0];cells={x['cell_id']:x for x in output['registry']['cells']};assert cells[r['replacement_cell_id']]['tenant_id']==r['tenant_id']
