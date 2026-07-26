import csv
from src.engine.tooling.strategy_factory.lcm.lcm_02.verify import verify_package

def test_reference_package(classification_root): assert verify_package(classification_root)['passed']
def test_all_artifacts_unique(classification_root):
 with (classification_root/'artifacts/artifact_classification_records.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
 assert len(rows)==len({r['artifact_path'] for r in rows})
def test_no_source_authority(classification_root):
 with (classification_root/'artifacts/artifact_classification_records.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
 assert not any(r['source_move_authorized']=='true' or r['source_delete_authorized']=='true' for r in rows)
def test_security_restricted(classification_root):
 with (classification_root/'artifacts/artifact_classification_records.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
 assert all(r['primary_disposition']=='SECURITY_RESTRICTED' for r in rows if r['security_sensitive']=='true')
def test_generated_noncanonical(classification_root):
 with (classification_root/'artifacts/artifact_classification_records.csv').open(encoding='utf-8',newline='') as f: rows=list(csv.DictReader(f))
 assert not any(r['generated_projection_canonical_authority']=='true' for r in rows)
