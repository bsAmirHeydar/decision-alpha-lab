#ifndef __EXP0018_DAYE_LIFECYCLE_IDENTITY_MQH__
#define __EXP0018_DAYE_LIFECYCLE_IDENTITY_MQH__

#include <DayeTrader/EXP0018/DAYE_LifecycleTypes.mqh>

string DAYE_BuildReferenceLifecycleId(const string reference_period_instance_id,
                                      const DAYE_HuntSide side,
                                      const string canonical_symbol_a,
                                      const string canonical_symbol_b)
{
   return "EXP0018|P07|REFERENCE|" + reference_period_instance_id + "|" +
          DAYE_HuntSideToString(side) + "|" + canonical_symbol_a + "|" + canonical_symbol_b;
}

string DAYE_BuildExactOpportunityUseKey(const DAYE_ConfirmationResult &result)
{
   return result.opportunity_id + "|" + DAYE_HuntSideToString(result.side) + "|" +
          result.hunter_canonical_symbol + "|" + result.protected_canonical_symbol;
}

string DAYE_BuildReferenceUseId(const DAYE_ConfirmationResult &result)
{
   return "EXP0018|P07|USE|" + result.result_id;
}

string DAYE_BuildLifecycleEventId(const DAYE_LifecycleEventType event_type,
                                  const string reference_id,
                                  const string evidence_id,
                                  const datetime event_time_utc)
{
   return "EXP0018|P07|EVENT|" + DAYE_LifecycleEventTypeToString(event_type) + "|" +
          reference_id + "|" + evidence_id + "|" + IntegerToString((int)event_time_utc);
}

bool DAYE_IsReferenceRetiredState(const DAYE_ReferenceLifecycleState state)
{
   return state == DAYE_REF_STATE_RETIRED_PROTECTED_TOUCH ||
          state == DAYE_REF_STATE_RETIRED_DOUBLE_HUNT ||
          state == DAYE_REF_STATE_RETIRED_ROLE_SWITCH;
}

#endif
