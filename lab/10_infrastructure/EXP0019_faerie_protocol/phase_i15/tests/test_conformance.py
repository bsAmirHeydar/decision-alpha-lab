from fp_i15_paper import *
def test_plan_conformance(buy_plan): assert assert_plan(buy_plan)
def test_run_conformance(buy_plan,buy_quote): assert assert_run(simulate(buy_plan,paper_policy(PaperPolicyProfile.FILLED),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms))
def test_registry_contracts(): assert len(registry()['public_contracts'])==20 and registry()['live_policy']=='UNSET'
