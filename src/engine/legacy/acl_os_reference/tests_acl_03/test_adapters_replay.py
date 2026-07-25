import copy,pytest
from tools.strategy_factory.acl_os.acl_03.known_time_ir import compile_known_time_ir
from tools.strategy_factory.acl_os.acl_03.feature_binding_ir import compile_feature_binding_ir
from tools.strategy_factory.acl_os.acl_03.detector_ir import compile_detector_ir
from tools.strategy_factory.acl_os.acl_03.adapters import compile_adapter_contracts
from tools.strategy_factory.acl_os.acl_03.golden_replay import compile_golden_cases,run_golden_replay,replay_case
from tools.strategy_factory.acl_os.acl_03.errors import ReplayError

def test_adapter_capabilities_are_non_trading(package):
    k,_=compile_known_time_ir(package);f,_=compile_feature_binding_ir(package);items=compile_adapter_contracts(package,k,f);assert items
    for x in items: assert x["capabilities"]["order_submission"] is False and x["capabilities"]["capital_access"] is False

def test_all_golden_cases_pass(context_root,package):
    d,_=compile_detector_ir(package);k,_=compile_known_time_ir(package);cases=compile_golden_cases(context_root,package,d);r=run_golden_replay(d,k,cases);assert r["case_count"]==3;assert r["failed_count"]==0

def test_replay_is_deterministic(context_root,package):
    d,_=compile_detector_ir(package);k,_=compile_known_time_ir(package);cases=compile_golden_cases(context_root,package,d);assert run_golden_replay(d,k,cases)==run_golden_replay(d,k,cases)

def test_known_time_regression_is_rejected(context_root,package):
    d,_=compile_detector_ir(package);k,_=compile_known_time_ir(package);case=compile_golden_cases(context_root,package,d)[0];case=copy.deepcopy(case);case["events"].append({"event":"X","known_time":"2020-01-01T00:00:00Z","decision_time":"2020-01-01T00:00:00Z","guard_result":True})
    with pytest.raises(ReplayError): replay_case(d,k,case)

def test_future_known_time_is_rejected(context_root,package):
    d,_=compile_detector_ir(package);k,_=compile_known_time_ir(package);case=copy.deepcopy(compile_golden_cases(context_root,package,d)[0]);case["events"][0]["known_time"]="2026-01-01T15:00:00Z";case["events"][0]["decision_time"]="2026-01-01T14:00:00Z"
    with pytest.raises(ReplayError): replay_case(d,k,case)
