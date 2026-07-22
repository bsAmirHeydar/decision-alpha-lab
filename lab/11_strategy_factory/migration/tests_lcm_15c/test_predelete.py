import json
def test_predelete(package_root):d=json.loads((package_root/'pre_delete_receipt.json').read_text());assert (d['candidate_count'],d['approved_deletion_count'],d['final_deletion_path_count'])==(2168,0,0)
