#ifndef __SF18_ACCOUNT_GUARD_SNAPSHOT_MQH__
#define __SF18_ACCOUNT_GUARD_SNAPSHOT_MQH__
#include "SF18_SafetyPolicy.mqh"
struct SF18_AccountGuardSnapshot
{
 long account_login;string account_server;double equity_cash,balance_cash,free_margin_cash,margin_level_percent,daily_realized_pnl_cash,floating_pnl_cash,total_exposure_volume;
 int active_order_count,open_position_count;bool terminal_trade_allowed,account_trade_allowed,expert_trade_allowed;long snapshot_time_utc_msc;string snapshot_hash;
};
string SF18_AccountSnapshotCanonical(const SF18_AccountGuardSnapshot &a)
{
 return IntegerToString(a.account_login)+"|"+a.account_server+"|"+SF01_CanonicalDouble(a.equity_cash)+"|"+SF01_CanonicalDouble(a.balance_cash)+"|"+
 SF01_CanonicalDouble(a.free_margin_cash)+"|"+SF01_CanonicalDouble(a.margin_level_percent)+"|"+SF01_CanonicalDouble(a.daily_realized_pnl_cash)+"|"+
 SF01_CanonicalDouble(a.floating_pnl_cash)+"|"+SF01_CanonicalDouble(a.total_exposure_volume)+"|"+IntegerToString(a.active_order_count)+"|"+
 IntegerToString(a.open_position_count)+"|"+SF01_CanonicalBool(a.terminal_trade_allowed)+"|"+SF01_CanonicalBool(a.account_trade_allowed)+"|"+
 SF01_CanonicalBool(a.expert_trade_allowed)+"|"+IntegerToString(a.snapshot_time_utc_msc);
}
string SF18_DeriveAccountSnapshotHash(const SF18_AccountGuardSnapshot &a){return SF01_StableId("acct",SF18_AccountSnapshotCanonical(a));}
bool SF18_ReadTerminalAccountSnapshot(const long now_utc_msc,SF18_AccountGuardSnapshot &a,string &error)
{
 a.account_login=AccountInfoInteger(ACCOUNT_LOGIN);a.account_server=AccountInfoString(ACCOUNT_SERVER);a.equity_cash=AccountInfoDouble(ACCOUNT_EQUITY);a.balance_cash=AccountInfoDouble(ACCOUNT_BALANCE);
 a.free_margin_cash=AccountInfoDouble(ACCOUNT_MARGIN_FREE);a.margin_level_percent=AccountInfoDouble(ACCOUNT_MARGIN_LEVEL);a.daily_realized_pnl_cash=0.0;a.floating_pnl_cash=AccountInfoDouble(ACCOUNT_PROFIT);
 a.total_exposure_volume=0.0;a.active_order_count=OrdersTotal();a.open_position_count=PositionsTotal();a.terminal_trade_allowed=(bool)TerminalInfoInteger(TERMINAL_TRADE_ALLOWED);
 a.account_trade_allowed=(bool)AccountInfoInteger(ACCOUNT_TRADE_ALLOWED);a.expert_trade_allowed=(bool)MQLInfoInteger(MQL_TRADE_ALLOWED);a.snapshot_time_utc_msc=now_utc_msc;a.snapshot_hash=SF18_DeriveAccountSnapshotHash(a);
 if(a.account_login<=0||a.account_server==""||a.equity_cash<0.0||a.free_margin_cash<0.0){error="invalid terminal account snapshot";return false;}error="";return true;
}
#endif
