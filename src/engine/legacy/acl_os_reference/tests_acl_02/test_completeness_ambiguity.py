import pytest
from src.engine.tooling.strategy_factory.acl_os.acl_02.loader import ContextPackageLoader
from src.engine.tooling.strategy_factory.acl_os.acl_02.completeness import evaluate_completeness
from src.engine.tooling.strategy_factory.acl_os.acl_02.ambiguity import AmbiguityAnalyzer

def load(root):
 p=ContextPackageLoader(root).load();p.pop("_paths");return p
def test_valid_completeness(valid_root):
 r=evaluate_completeness(load(valid_root));assert r["overall_score"]==1;assert r["blocking_count"]==0
def test_incomplete_detected(valid_root):
 root=valid_root.parent/"incomplete_context";r=evaluate_completeness(load(root));assert r["blocking_count"]>=1
def test_ambiguity_detected(valid_root):
 r=AmbiguityAnalyzer().analyze(load(valid_root.parent/"ambiguous_context"));assert r["blocking_count"]>=1
@pytest.mark.parametrize("token",["significant","strong","clean","valid","soon","near","usually","etc","good","bad"])
def test_vague_term_catalog_enforced(valid_root,token):
 p=load(valid_root);p["occurrence"]["start_rule"]="A "+token+" move with otherwise deterministic clocks and inputs";r=AmbiguityAnalyzer().analyze(p);assert any(x["code"]=="ACL02_VAGUE_TERM" for x in r["findings"])
