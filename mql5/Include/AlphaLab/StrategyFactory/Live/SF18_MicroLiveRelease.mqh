#ifndef __SF18_MICRO_LIVE_RELEASE_MQH__
#define __SF18_MICRO_LIVE_RELEASE_MQH__
#include "../Contracts/SF01_Hash.mqh"
#include "../Contracts/SF01_StringCodec.mqh"
struct SF18_MicroLiveRelease
{
 string release_id,release_version,strategy_id,strategy_version,model_release_hash,decision_policy_hash,risk_policy_hash,allocation_policy_hash,execution_policy_hash;
 long runtime_generation_id,account_login;string account_server,allowed_symbol;double maximum_volume;int maximum_orders;long valid_from_utc_msc,valid_until_utc_msc;
 string phase17_soak_evidence_hash,reconciliation_evidence_hash,anti_overfit_evidence_hash,release_hash;
};
string SF18_ReleaseCanonical(const SF18_MicroLiveRelease &r)
{
 return r.release_id+"|"+r.release_version+"|"+r.strategy_id+"|"+r.strategy_version+"|"+IntegerToString(r.runtime_generation_id)+"|"+
 r.model_release_hash+"|"+r.decision_policy_hash+"|"+r.risk_policy_hash+"|"+r.allocation_policy_hash+"|"+r.execution_policy_hash+"|"+
 IntegerToString(r.account_login)+"|"+r.account_server+"|"+r.allowed_symbol+"|"+SF01_CanonicalDouble(r.maximum_volume)+"|"+IntegerToString(r.maximum_orders)+"|"+
 IntegerToString(r.valid_from_utc_msc)+"|"+IntegerToString(r.valid_until_utc_msc)+"|"+r.phase17_soak_evidence_hash+"|"+r.reconciliation_evidence_hash+"|"+r.anti_overfit_evidence_hash;
}
string SF18_DeriveReleaseHash(const SF18_MicroLiveRelease &r){return SF01_StableId("lrel",SF18_ReleaseCanonical(r));}
bool SF18_ValidateRelease(const SF18_MicroLiveRelease &r,string &error)
{
 if(!SF01_IsSafeIdentifier(r.release_id)||!SF01_IsSafeIdentifier(r.release_version)||!SF01_IsSafeIdentifier(r.strategy_id)||!SF01_IsSafeIdentifier(r.strategy_version)||!SF01_IsTerminalSymbol(r.allowed_symbol)){error="invalid release identity";return false;}
 if(r.runtime_generation_id<0||r.account_login<=0||r.account_server==""||r.maximum_volume<=0.0||r.maximum_orders<=0||r.valid_until_utc_msc<=r.valid_from_utc_msc){error="invalid release bounds";return false;}
 const string expected=SF18_DeriveReleaseHash(r);if(r.release_hash!=""&&r.release_hash!=expected){error="release hash mismatch";return false;}error="";return true;
}
#endif
