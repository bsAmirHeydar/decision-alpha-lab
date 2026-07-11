#ifndef __SF18_LIVE_AUTHORIZATION_MQH__
#define __SF18_LIVE_AUTHORIZATION_MQH__
#include "SF18_MicroLiveRelease.mqh"
#include "SF18_LiveEnums.mqh"
struct SF18_LiveAuthorization
{
 string authorization_id,release_hash;long account_login;string account_server,allowed_symbol;ENUM_SF18_LIVE_MODE mode;
 long issued_at_utc_msc,expires_at_utc_msc;double maximum_volume;int maximum_orders;string nonce,operator_token_hash,authorization_hash;
};
string SF18_AuthorizationCanonical(const SF18_LiveAuthorization &a)
{
 return a.authorization_id+"|"+a.release_hash+"|"+IntegerToString(a.account_login)+"|"+a.account_server+"|"+a.allowed_symbol+"|"+
 IntegerToString((int)a.mode)+"|"+IntegerToString(a.issued_at_utc_msc)+"|"+IntegerToString(a.expires_at_utc_msc)+"|"+
 SF01_CanonicalDouble(a.maximum_volume)+"|"+IntegerToString(a.maximum_orders)+"|"+a.nonce+"|"+a.operator_token_hash;
}
string SF18_DeriveAuthorizationHash(const SF18_LiveAuthorization &a){return SF01_StableId("lauth",SF18_AuthorizationCanonical(a));}
bool SF18_ValidateAuthorization(const SF18_LiveAuthorization &a,string &error)
{
 if(!SF01_IsSafeIdentifier(a.authorization_id)||!SF01_IsSafeIdentifier(a.release_hash)||!SF01_IsTerminalSymbol(a.allowed_symbol)||a.account_server==""||!SF01_IsSafeIdentifier(a.nonce)||!SF01_IsSafeIdentifier(a.operator_token_hash)){error="invalid authorization identity";return false;}
 if(a.account_login<=0||(a.mode!=SF18_LIVE_DRY_RUN&&a.mode!=SF18_LIVE_MICRO)||a.expires_at_utc_msc<=a.issued_at_utc_msc||a.maximum_volume<=0.0||a.maximum_orders<=0){error="invalid authorization bounds";return false;}
 const string expected=SF18_DeriveAuthorizationHash(a);if(a.authorization_hash!=""&&a.authorization_hash!=expected){error="authorization hash mismatch";return false;}error="";return true;
}
#endif
