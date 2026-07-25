import pytest
from fp_i15_paper import *
@pytest.mark.parametrize('profile,expected',[
(PaperPolicyProfile.PLAN_CREATED,QuotaState.CONSUMED),(PaperPolicyProfile.ORDER_ATTEMPTED,QuotaState.CONSUMED),(PaperPolicyProfile.ORDER_ACCEPTED,QuotaState.CONSUMED),(PaperPolicyProfile.FILLED,QuotaState.CONSUMED),(PaperPolicyProfile.TWO_STAGE_ACCEPTED,QuotaState.CONSUMED),(PaperPolicyProfile.TWO_STAGE_FILLED,QuotaState.CONSUMED)])
def test_immediate_fill_consumes_all_profiles(buy_plan,buy_quote,profile,expected): assert simulate(buy_plan,paper_policy(profile),PaperScenario.IMMEDIATE_FILL,buy_quote,buy_plan.created_utc_ms).quota.state==expected
@pytest.mark.parametrize('profile,expected',[
(PaperPolicyProfile.PLAN_CREATED,QuotaState.CONSUMED),(PaperPolicyProfile.ORDER_ATTEMPTED,QuotaState.CONSUMED),(PaperPolicyProfile.ORDER_ACCEPTED,QuotaState.RELEASED),(PaperPolicyProfile.FILLED,QuotaState.RELEASED),(PaperPolicyProfile.TWO_STAGE_ACCEPTED,QuotaState.RELEASED),(PaperPolicyProfile.TWO_STAGE_FILLED,QuotaState.RELEASED)])
def test_rejection_profile_behavior(buy_plan,buy_quote,profile,expected): assert simulate(buy_plan,paper_policy(profile),PaperScenario.REJECT_AT_ATTEMPT,buy_quote,buy_plan.created_utc_ms).quota.state==expected
