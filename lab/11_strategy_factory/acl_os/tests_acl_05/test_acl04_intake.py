import json, shutil
import pytest
from tools.strategy_factory.acl_os.acl_05.handoff_input import load_acl04_bundle

def copy_tree(src,dst): shutil.copytree(src,dst); return dst

def test_acl04_bundle_valid(acl04_root):
    b=load_acl04_bundle(acl04_root); assert len(b["candidates"])==12

def test_missing_marker_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); (root/".acl04_generated_root").unlink()
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_wrong_handoff_type_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); p=root/"handoff/acl05_handoff.json"; d=json.load(open(p)); d["handoff_type"]="WRONG"; p.write_text(json.dumps(d))
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_candidate_byte_tamper_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); p=next((root/"candidates/canonical").glob("*.json")); p.write_text(p.read_text()+" ")
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_manifest_digest_tamper_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); p=root/"output_manifest.json"; d=json.load(open(p)); d["artifact_count"]+=1; p.write_text(json.dumps(d))
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_receipt_tamper_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); p=root/"factory_receipt.json"; d=json.load(open(p)); d["canonical_candidate_count"]+=1; p.write_text(json.dumps(d))
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_missing_candidate_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); next((root/"candidates/canonical").glob("*.json")).unlink()
    with pytest.raises(Exception): load_acl04_bundle(root)

def test_manifest_path_escape_denied(tmp_path,acl04_root):
    root=copy_tree(acl04_root,tmp_path/"acl04"); p=root/"output_manifest.json"; d=json.load(open(p)); d["files"][0]["path"]="../escape"; p.write_text(json.dumps(d))
    with pytest.raises(Exception): load_acl04_bundle(root)
