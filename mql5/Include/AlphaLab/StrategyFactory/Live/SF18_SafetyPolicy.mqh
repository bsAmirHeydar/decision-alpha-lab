#ifndef __SF18_SAFETY_POLICY_MQH__
#define __SF18_SAFETY_POLICY_MQH__
#include "SF18_LiveAuthorization.mqh"
struct SF18_SafetyPolicy
{
 string policy_id,policy_version;int maximum_orders_per_session,maximum_concurrent_orders,maximum_positions;
 double maximum_volume_per_order,maximum_total_exposure_volume,maximum_cash_risk_per_order,maximum_daily_realized_loss_cash,maximum_daily_total_loss_cash;
 double minimum_equity_cash,minimum_free_margin_cash,minimum_margin_level_percent,maximum_spread_points;
 long maximum_quote_age_milliseconds,maximum_account_snapshot_age_milliseconds;int maximum_deviation_points,maximum_consecutive_failures;
 long cooldown_after_failure_milliseconds;bool one_shot_authorization,require_terminal_permission,require_account_permission,allow_emergency_flatten;string policy_hash;
};
string SF18_SafetyPolicyCanonical(const SF18_SafetyPolicy &p)
{
 return p.policy_id+"|"+p.policy_version+"|"+IntegerToString(p.maximum_orders_per_session)+"|"+IntegerToString(p.maximum_concurrent_orders)+"|"+IntegerToString(p.maximum_positions)+"|"+
 SF01_CanonicalDouble(p.maximum_volume_per_order)+"|"+SF01_CanonicalDouble(p.maximum_total_exposure_volume)+"|"+SF01_CanonicalDouble(p.maximum_cash_risk_per_order)+"|"+
 SF01_CanonicalDouble(p.maximum_daily_realized_loss_cash)+"|"+SF01_CanonicalDouble(p.maximum_daily_total_loss_cash)+"|"+SF01_CanonicalDouble(p.minimum_equity_cash)+"|"+
 SF01_CanonicalDouble(p.minimum_free_margin_cash)+"|"+SF01_CanonicalDouble(p.minimum_margin_level_percent)+"|"+SF01_CanonicalDouble(p.maximum_spread_points)+"|"+
 IntegerToString(p.maximum_quote_age_milliseconds)+"|"+IntegerToString(p.maximum_account_snapshot_age_milliseconds)+"|"+IntegerToString(p.maximum_deviation_points)+"|"+
 IntegerToString(p.maximum_consecutive_failures)+"|"+IntegerToString(p.cooldown_after_failure_milliseconds)+"|"+SF01_CanonicalBool(p.one_shot_authorization)+"|"+
 SF01_CanonicalBool(p.require_terminal_permission)+"|"+SF01_CanonicalBool(p.require_account_permission)+"|"+SF01_CanonicalBool(p.allow_emergency_flatten);
}
string SF18_DeriveSafetyPolicyHash(const SF18_SafetyPolicy &p){return SF01_StableId("lpol",SF18_SafetyPolicyCanonical(p));}
bool SF18_ValidateSafetyPolicy(const SF18_SafetyPolicy &p,string &error)
{
 if(!SF01_IsSafeIdentifier(p.policy_id)||!SF01_IsSafeIdentifier(p.policy_version)){error="invalid safety policy identity";return false;}
 if(p.maximum_orders_per_session<=0||p.maximum_concurrent_orders<0||p.maximum_positions<0||p.maximum_volume_per_order<=0.0||p.maximum_total_exposure_volume<=0.0||p.maximum_cash_risk_per_order<=0.0||p.maximum_consecutive_failures<=0){error="invalid safety policy bounds";return false;}
 if(p.maximum_daily_realized_loss_cash<0.0||p.maximum_daily_total_loss_cash<0.0||p.minimum_equity_cash<0.0||p.minimum_free_margin_cash<0.0||p.minimum_margin_level_percent<0.0||p.maximum_spread_points<0.0||p.maximum_quote_age_milliseconds<0||p.maximum_account_snapshot_age_milliseconds<0||p.maximum_deviation_points<0||p.cooldown_after_failure_milliseconds<0){error="negative safety bound";return false;}
 const string expected=SF18_DeriveSafetyPolicyHash(p);if(p.policy_hash!=""&&p.policy_hash!=expected){error="safety policy hash mismatch";return false;}error="";return true;
}
#endif
