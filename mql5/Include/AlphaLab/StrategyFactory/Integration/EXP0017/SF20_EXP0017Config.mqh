#ifndef __SF20_EXP0017_CONFIG_MQH__
#define __SF20_EXP0017_CONFIG_MQH__
#include "../../Contracts/SF01_AllContracts.mqh"
#include "SF20_EXP0017Enums.mqh"
#include <IntermarketDivergenceExecution/CG/CGT_Types.mqh>
#define SF20_EXP0017_PLUGIN_ID "sf20.exp0017.temporal_intermarket_divergence"
#define SF20_EXP0017_PLUGIN_VERSION "1.0.0"
struct SF20_EXP0017Config
{
 string symbol_a,symbol_b;int broker_utc_offset_hours;bool use_auto_new_york_dst;int manual_new_york_utc_offset_hours;ulong group_mask;bool require_m1_history;int m1_lookback_bars;ENUM_SF20_INTEGRATION_MODE mode;bool live_authority;
};
ulong SF20_AllGroupMask(){ulong mask=0;for(int i=0;i<CGT_GROUP_COUNT;i++)mask|=((ulong)1<<i);return mask;}
bool SF20_GroupEnabled(const ulong mask,const int index){if(index<0||index>=CGT_GROUP_COUNT)return false;return (mask&((ulong)1<<index))!=0;}
SF20_EXP0017Config SF20_DefaultEXP0017Config()
{
 SF20_EXP0017Config c;c.symbol_a="SPXUSD";c.symbol_b="NDXUSD";c.broker_utc_offset_hours=3;c.use_auto_new_york_dst=true;c.manual_new_york_utc_offset_hours=-5;c.group_mask=SF20_AllGroupMask();c.require_m1_history=true;c.m1_lookback_bars=1600;c.mode=SF20_MODE_AUDIT_ONLY;c.live_authority=false;return c;
}
string SF20_EXP0017ConfigCanonical(const SF20_EXP0017Config &c)
{return c.symbol_a+"|"+c.symbol_b+"|"+IntegerToString(c.broker_utc_offset_hours)+"|"+SF01_CanonicalBool(c.use_auto_new_york_dst)+"|"+IntegerToString(c.manual_new_york_utc_offset_hours)+"|"+IntegerToString((long)c.group_mask)+"|"+SF01_CanonicalBool(c.require_m1_history)+"|"+IntegerToString(c.m1_lookback_bars)+"|"+IntegerToString((int)c.mode)+"|"+SF01_CanonicalBool(c.live_authority);}
string SF20_EXP0017ConfigHash(const SF20_EXP0017Config &c){return SF01_StableId("sf20cfg",SF20_EXP0017ConfigCanonical(c));}
bool SF20_ValidateEXP0017Config(const SF20_EXP0017Config &c,string &error)
{
 if(!SF01_IsSafeTerminalSymbol(c.symbol_a,64)||!SF01_IsSafeTerminalSymbol(c.symbol_b,64)||c.symbol_a==c.symbol_b){error="invalid symbol pair";return false;}
 if(c.broker_utc_offset_hours<-14||c.broker_utc_offset_hours>14||c.manual_new_york_utc_offset_hours<-14||c.manual_new_york_utc_offset_hours>14){error="invalid UTC offset";return false;}
 if(c.group_mask==0){error="no cycle group enabled";return false;}if(c.m1_lookback_bars<16||c.m1_lookback_bars>100000){error="invalid M1 lookback";return false;}
 if(c.live_authority){error="Phase 20 live authority must remain false";return false;}error="";return true;
}
#endif
