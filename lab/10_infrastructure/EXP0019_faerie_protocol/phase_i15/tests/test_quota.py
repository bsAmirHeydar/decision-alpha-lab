import pytest
from fp_i15_paper import *
def test_reserve_available(buy_plan): assert PaperQuotaStore().reserve(buy_plan,paper_policy(PaperPolicyProfile.FILLED)).state==QuotaState.RESERVED
def test_plan_policy_consumes_immediately(buy_plan): assert PaperQuotaStore().reserve(buy_plan,paper_policy(PaperPolicyProfile.PLAN_CREATED)).state==QuotaState.CONSUMED
def test_duplicate_reserve_idempotent(buy_plan):
 s=PaperQuotaStore();p=paper_policy(PaperPolicyProfile.FILLED);a=s.reserve(buy_plan,p);b=s.reserve(buy_plan,p);assert a.record_hash==b.record_hash
def test_second_signal_cannot_reserve(buy_plan,sell_plan):
 s=PaperQuotaStore();p=paper_policy(PaperPolicyProfile.FILLED);s.reserve(buy_plan,p)
 from dataclasses import replace
 with pytest.raises(FPI15Error): s.reserve(replace(sell_plan,quota_key_id=buy_plan.quota_key_id),p)
def test_release_allowed_before_fill(buy_plan):
 s=PaperQuotaStore();p=paper_policy(PaperPolicyProfile.FILLED);s.reserve(buy_plan,p);assert s.release(buy_plan.quota_key_id,p,'FP_PAPER_ORDER_REJECTED').state==QuotaState.RELEASED
def test_release_forbidden_after_consumption(buy_plan):
 s=PaperQuotaStore();p=paper_policy(PaperPolicyProfile.PLAN_CREATED);s.reserve(buy_plan,p);assert s.release(buy_plan.quota_key_id,p,'FP_PAPER_ORDER_REJECTED').state==QuotaState.CONSUMED
def test_unset_policy_rejected(buy_plan):
 with pytest.raises(FPI15Error): PaperQuotaStore().reserve(buy_plan,paper_policy(PaperPolicyProfile.UNSET))
