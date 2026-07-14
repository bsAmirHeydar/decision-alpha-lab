from .contracts import *

def paper_policy(profile:PaperPolicyProfile)->PaperPolicyConfig:
    pre=frozenset({"FP_PAPER_QUOTE_UNAVAILABLE","FP_PAPER_GEOMETRY_REVALIDATION_FAILED","FP_PAPER_LOCAL_VALIDATION_FAILED","FP_PAPER_PLAN_BLOCKED"})
    if profile==PaperPolicyProfile.UNSET: return PaperPolicyConfig(profile,PaperConsumeEvent.UNSET,frozenset())
    if profile==PaperPolicyProfile.PLAN_CREATED: return PaperPolicyConfig(profile,PaperConsumeEvent.PLAN_CREATED,frozenset())
    if profile==PaperPolicyProfile.ORDER_ATTEMPTED: return PaperPolicyConfig(profile,PaperConsumeEvent.ORDER_ATTEMPTED,pre)
    if profile in (PaperPolicyProfile.ORDER_ACCEPTED,PaperPolicyProfile.TWO_STAGE_ACCEPTED): return PaperPolicyConfig(profile,PaperConsumeEvent.ORDER_ACCEPTED,pre|{"FP_PAPER_ORDER_REJECTED"})
    if profile in (PaperPolicyProfile.FILLED,PaperPolicyProfile.TWO_STAGE_FILLED): return PaperPolicyConfig(profile,PaperConsumeEvent.FIRST_FILL,pre|{"FP_PAPER_ORDER_REJECTED","FP_PAPER_ORDER_CANCELLED","FP_PAPER_UNFILLED_EXPIRED"})
    raise ValueError(profile)
