import pytest
@pytest.mark.parametrize("cell_idx",range(128))
def test_every_cell_is_reconciled(reference_output,cell_idx):
 row=reference_output["reconciliation"]["rows"][cell_idx];assert row["reconciled"] is True
@pytest.mark.parametrize("cell_idx",range(128))
def test_every_cell_has_isolation_proof(reference_output,cell_idx):
 row=reference_output["isolation"]["rows"][cell_idx];assert row["cross_tenant_allowed"] is False;assert row["cross_namespace_allowed"] is False
@pytest.mark.parametrize("tenant_idx",range(8))
def test_tenant_has_sixteen_cells(reference_output,tenant_idx):
 tenant=f"TENANT_{tenant_idx+1:02d}";assert reference_output["registry_index"]["tenant_rows"][tenant_idx]["tenant_id"]==tenant;assert reference_output["registry_index"]["tenant_rows"][tenant_idx]["cell_count"]==16
@pytest.mark.parametrize("domain",["FD_EU_A","FD_EU_B","FD_EU_C","FD_EU_D","FD_US_A","FD_US_B","FD_US_C","FD_US_D"])
def test_failure_domain_used(reference_output,domain):assert reference_output["placement"]["domain_usage"][domain]>0
@pytest.mark.parametrize("idx",range(64))
def test_route_event_hash_chain(reference_output,idx):
 e=reference_output["route_ledger"]["events"][idx];assert len(e["event_hash"])==64;assert e["ordinal"]==idx
