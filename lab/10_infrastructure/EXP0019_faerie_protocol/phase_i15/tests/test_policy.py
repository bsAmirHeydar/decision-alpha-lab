import pytest
from fp_i15_paper import *
@pytest.mark.parametrize('profile,event',[
(PaperPolicyProfile.PLAN_CREATED,PaperConsumeEvent.PLAN_CREATED),(PaperPolicyProfile.ORDER_ATTEMPTED,PaperConsumeEvent.ORDER_ATTEMPTED),(PaperPolicyProfile.ORDER_ACCEPTED,PaperConsumeEvent.ORDER_ACCEPTED),(PaperPolicyProfile.FILLED,PaperConsumeEvent.FIRST_FILL),(PaperPolicyProfile.TWO_STAGE_ACCEPTED,PaperConsumeEvent.ORDER_ACCEPTED),(PaperPolicyProfile.TWO_STAGE_FILLED,PaperConsumeEvent.FIRST_FILL)])
def test_policy_mapping(profile,event): assert paper_policy(profile).consume_event==event
def test_unset_profile_remains_unset(): assert paper_policy(PaperPolicyProfile.UNSET).consume_event==PaperConsumeEvent.UNSET
def test_live_policy_constant_unset(): assert LIVE_QUOTA_POLICY=='UNSET' and LIVE_EXECUTION_ENABLED is False
