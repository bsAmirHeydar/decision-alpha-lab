import copy,pytest
from src.engine.tooling.strategy_factory.acl_os.acl_02.loader import ContextPackageLoader
from src.engine.tooling.strategy_factory.acl_os.acl_02.clocks import validate_causal_clock
from src.engine.tooling.strategy_factory.acl_os.acl_02.semantics import validate_semantics

def pkg(root):p=ContextPackageLoader(root).load();p.pop("_paths");return p
def test_clock_pass(valid_root):assert validate_causal_clock(pkg(valid_root)["causal_clock"])["passed"]
@pytest.mark.parametrize("name",["event_time","observation_time","known_time","decision_time","maturity_time","correction_time"])
def test_each_clock_required(valid_root,name):
 c=copy.deepcopy(pkg(valid_root)["causal_clock"]);del c["clocks"][name];assert not validate_causal_clock(c)["passed"]
def test_future_revision_forbidden(valid_root):
 c=copy.deepcopy(pkg(valid_root)["causal_clock"]);c["clocks"]["known_time"]["can_use_future_revision"]=True;assert not validate_causal_clock(c)["passed"]
def test_semantics_pass(valid_root):assert validate_semantics(pkg(valid_root))["passed"]
def test_goal_conflict_is_ambiguity(valid_root):
 from src.engine.tooling.strategy_factory.acl_os.acl_02.ambiguity import AmbiguityAnalyzer
 p=pkg(valid_root);p["scope"]["goals"]=[p["scope"]["non_goals"][0]];assert AmbiguityAnalyzer().analyze(p)["blocking_count"]>0
