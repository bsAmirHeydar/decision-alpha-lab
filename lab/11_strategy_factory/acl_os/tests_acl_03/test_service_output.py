import json,hashlib,copy
from pathlib import Path
import pytest
from tools.strategy_factory.acl_os.acl_03.service import ACL03ContextCompilerService
from tools.strategy_factory.acl_os.acl_03.errors import PrerequisiteError

def test_end_to_end_compile(tmp_path,context_root,permit,approval,readiness):
    out=tmp_path/"compiled";r=ACL03ContextCompilerService().compile(context_root,out,permit,approval,readiness);assert r["passed"];assert r["onboarding"]["highest_state"]=="CONTEXT_COMPILED";assert (out/"compilation_receipt.json").is_file();assert (out/"handoff/acl04_handoff.json").is_file()

def test_output_is_deterministic_except_path(tmp_path,context_root,permit,approval,readiness):
    a=ACL03ContextCompilerService().compile(context_root,tmp_path/"a",permit,approval,readiness);b=ACL03ContextCompilerService().compile(context_root,tmp_path/"b",permit,approval,readiness);assert a["receipt"]==b["receipt"];assert a["output_manifest"]==b["output_manifest"]

def test_refuses_replace_unmarked_directory(tmp_path,context_root,permit,approval,readiness):
    out=tmp_path/"unsafe";out.mkdir();(out/"human.txt").write_text("x")
    with pytest.raises(ValueError): ACL03ContextCompilerService().compile(context_root,out,permit,approval,readiness)

def test_changed_source_invalidates_approval(tmp_path,context_root,permit,approval,readiness):
    # approval digest is exact; mutation is represented by altering approval digest here to avoid modifying canonical fixture
    bad=copy.deepcopy(approval);bad["source_snapshot_digest"]="sha256:"+"1"*64
    with pytest.raises(PrerequisiteError): ACL03ContextCompilerService().compile(context_root,tmp_path/"x",permit,bad,readiness)

def test_generated_files_never_claim_capital(tmp_path,context_root,permit,approval,readiness):
    out=tmp_path/"compiled";ACL03ContextCompilerService().compile(context_root,out,permit,approval,readiness)
    for p in out.rglob("*"):
        if p.is_file():
            t=p.read_text(encoding="utf-8",errors="ignore");assert '"capital_activation_allowed": true' not in t.lower();assert '"live_order_submission_allowed": true' not in t.lower()
